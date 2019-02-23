"""
    DBOperation module has all the functions that involve all MongoDB operations.
    In general, all the CRUD operations business logic will be implemented here.
    Each and every application will call functions from DBOperation to perform database tasks.
"""
import logging as log

import pymongo

from lib.exceptions.duplicate_key_error import DuplicateKeyError
from pylib.factories import container
from views.contrib.validations import save_if_valid

db = container.get('db')


def _import_from(name):
    """
    tries to import a list schema classes from models.documents
    """
    module = "models.documents"
    module = __import__(module, fromlist=[name])

    return module


def _dereference(ref):
    """
    tries to find a document in database with given reference
    """
    _dbname = ref.database
    collname = ref.collection

    return db[collname].find_one({'_id': ref.id})


def dereference(ref):
    return db.dereference(ref)


def __is_dereferancable(self, ref):
    """
    Tries to access the id variable associated to the dbref object
    """
    try:
        _id = ref.id

        return True
    except Exception, err:
        return False


def read_count(collection, condition):
    """
    returns count of items in collection corresponding to the condition.
    """

    return db[collection.lower()].find(condition).count()


def read_db(_collection, _condition, _projection={'_id': 1}):
    """
    returns a list of documents with fields specified in projection that found in database satisfing the condition.
    schema will not be used!
    e.g.
    _collection = user
    _condition = {'active':True}
    _projection = {'username':1, 'active':1}
    will give result like this
    [{'username':'user1', 'active':True}, ...]
    """
    documents = list(db[_collection.lower()].find(_condition, _projection))

    return documents


def read_db_single(_collection, _condition, _projection={'_id': 0}, **kwargs):
    """
    returns a single document with fields specified in projection that found in database satisfing the condition.
    schema will not be used!
    e.g. 
    _collection = user
    _condition = {'active':True}
    _projection = {'username':1, 'active':1}
    will give result like this {'username':'user1', 'active':True}
    """
    document = db[_collection.lower()].find_one(_condition, _projection, **kwargs)
    return document


def read_user(condition):
    """returns user\'s document that satisfy the given condition.
    """
    return db.user.find_one(condition)


def get_count(collection, condition):
    """
    returns the count of documents in the database that satisfies the given condition
    """
    return db[collection.lower()].find(condition).count()


def create(collection_name, __multiple_create=False, **data):
    """ Creates a new document in database and returns the created document in a list.
    **Update**
    This method can also be used to create multiple entries using single create method

    **__multiple_create** if set to True will check for required key in data argument to
    get list of data to insert to mongo database

    returns tuple with first entry as boolean and second entry list in case of success and
    either list of dictionary or single dictionary according to __multiple_create value.
    If __multiple_create is set to True, it will return list of dictionary during any
    failure in database operation

    e.g for single entry
    data = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3"
        ...
    }
    e.g for multiple entry
    data = {
        "__multiple_create": True,
        "data": [dict_entry1, dict_entry2]
    }

    """
    module = _import_from(collection_name)

    if __multiple_create:
        data_list = data.get("data")
    else:
        data_list = [data]

    errors = []
    collection_objs = []
    for data in data_list:
        try:
            collection_obj = getattr(module, collection_name)()
            getattr(collection_obj, "update")(data)
            save_if_valid(collection_obj)
            collection_objs.append(collection_obj)
        except pymongo.errors.DuplicateKeyError as e:
            raise DuplicateKeyError()
        except Exception as e:
            log.warn(str(e))
            errors.append({'msg': str(e), 'condition': collection_name.lower()})

    if errors:
        if not __multiple_create:
            errors = errors[0]
        return False, errors

    return True, collection_objs


def rename(old_collection_name, new_collection_name):
    """
    renames the old collection to new one
    Note: It will clear all existing documents in new_collection and
    after moving documents from old_collection to new_collection
    old_collection also made empty
    :param old_collection_name: string, collection name
    :param new_collection_name: string, collection name
    :return: dict, mongo response: {"ok": 1} or { "ok" : 0, "errmsg" : [] }
    """

    cur_enrichmentsources = read(old_collection_name, {})
    if cur_enrichmentsources:
        delete(new_collection_name, {})
        status, response_data = create(new_collection_name, __multiple_create=True, data=cur_enrichmentsources)
        if status:
            delete(old_collection_name, {})
            response = {"ok": 1}
        else:
            response = {"ok": 0, "errmsg": response_data}
    else:
        response = {"ok": 0,
                    "errmsg": "dboperation; collection name old_collection_name=%s not found" % old_collection_name}
    # Dev_Note: Try to refactor ths code and find method to perform rename directly; response =  db[old_collection_name].rename(new_collection_name)
    return response


def read(collection_name, condition, _single=False):
    """
    returns the list if _single is False otherwise a single dict object reading from database for the given condition
    """
    module = _import_from(collection_name)

    collection_class = getattr(module, collection_name)
    if _single:
        collection_obj = getattr(collection_class, "find_one")(condition)
    else:
        collection_obj = getattr(collection_class.collection, "find")(condition)
        collection_obj = list(collection_obj)

    return collection_obj


def sorted_read(collection, query_condition, sort_criteria):
    """
    returns collection entries followed by the sorting criteria
    collection : collection name
    query_condition : {"username": "user"}
    sort_criteria : [["_id", -1]]
    """
    return list(db[collection.lower()].find(query_condition).sort(sort_criteria))


def delete(collection_name, condition):
    """
    tries to delete all the document in database that satisfies the condition
    """
    module = _import_from(collection_name)
    collection_class = getattr(module, collection_name)
    docs = list(getattr(collection_class, "find")(condition))
    errors = []
    response = {}
    for doc in docs:
        msg = getattr(doc, "delete")()
        if msg:
            # error occourred while deleting the item; is logging necessary?
            errors.append({"condition": str(condition), 'msg': msg})
            docs.remove(doc)
    response.update({'errors': errors, 'docs': docs})

    return response


def update(collection_name, docs, multi=False, single=False):
    """
    update(collection_name, condition, document, multi) => tuple
    updates the document in the collection. if multi is True, the condition is applied to multiple documents in the collection.
    """
    response = {}
    errors = []
    imported_module = _import_from(collection_name)
    if multi:
        docs = docs[0]
        condition = docs.get('condition')
        to_insert = docs.get("doc")
        msg = db[collection_name.lower()].update(condition, {"$set": to_insert}, multi=multi)
        if msg and msg.get('err'):
            errors.append({"msg": msg, "condition": str(condition)})
        response.update({"docs": [], "errors": errors})

        return response

    updated_docs = []
    for doc in docs:
        condition = doc.get("condition")
        doc = doc.get("doc")
        collection_class = getattr(imported_module, collection_name)
        collection_obj = getattr(collection_class, "find_one")(condition)
        if collection_obj:
            getattr(collection_obj, "update")(doc)
            msg = save_if_valid(collection_obj)
            if msg:
                errors.append({"condition": str(condition), "msg": msg})
            else:
                updated_docs.append({"doc": collection_obj})
        else:
            errors.append({"condition": str(condition), "msg": "not found"})
    response.update({"docs": updated_docs, "errors": errors})

    return response


def update_push(collection_name, condition, to_push):
    """
    pushes an element from an existing database document with the condition satisfied
    """
    to_push.pop("_id", None)
    db[collection_name.lower()].update(condition, {"$push": to_push})

    return True, True


def update_pull(collection_name, condition, to_pull, _id=False):
    """
    pulls an element from an existing document in database with the condition satisfied
    """
    if not _id:
        to_pull.pop("_id", None)
    db[collection_name.lower()].update(condition, {"$pull": to_pull}, multi=True)

    return True, True


def update_set(collection_name, condition, to_set_data):
    """
    sets a field in an existing document in database with the condition satisfied
    """
    db[collection_name.lower()].update(condition, {"$set": to_set_data})

    return True


def update_using_queries(collection_name, condition, queries, multi=False):
    """
    updates the document in the collection
    Note: used for aggregated queries or for new operators
    queries = {'$set': {'status': job_status}, '$push': {'errors': str(exception)}, '$inc': {'errors_count': 1}}
    """
    response = {}
    errors = []
    msg = db[collection_name.lower()].update(condition, queries, multi=multi)
    if msg and msg.get('err'):
        errors.append({'msg': msg, 'condition': str(condition)})
    response.update({'docs': [], 'errors': errors})
    return response
