from db import db
from google.cloud import firestore

# Firestore object
sleep_record_ref = db.collection(u'sleep')


def createSleepRecord(userid, start_time=None, end_time=None, sleep_rating=None, last_modified=None):
    sleep_dict = dict()
    sleep_dict['userid'] = userid
    sleep_dict['date'] = firestore.SERVER_TIMESTAMP
    sleep_dict['start_time'] = start_time
    sleep_dict['end_time'] = end_time
    sleep_dict['sleep_rating'] = sleep_rating
    sleep_dict['last_modified'] = last_modified

    sleep_record = sleep_record_ref.add(sleep_dict)


    return print(sleep_record)


def getUserSleepRecords(user_id):

    docs_ref = db.collection(u"sleep").where(u'userid', u'==', user_id).order_by(u"date", direction=firestore.Query.DESCENDING)

    docs = docs_ref.get()

    list = []
    for doc in docs:
        list.append(doc.to_dict())
    
    return list
    

def getLastSeven(user_id):
    
    # Uses composite index to order the documents
    docs_ref = db.collection(u"sleep").where(u'userid', u'==', user_id).order_by(u"date", direction=firestore.Query.DESCENDING)

    docs = docs_ref.limit(7).get()

    list = []
    for doc in docs:
        list.append(doc.to_dict())

    return list


def getLastThirty(user_id):

    # Uses composite index to order the documents
    docs_ref = db.collection(u"sleep").where(u'userid', u'==', user_id).order_by(u"date", direction=firestore.Query.DESCENDING)

    docs = docs_ref.limit(30).get()

    list = []
    for doc in docs:
        list.append(doc.to_dict())

    return list
    


def updateSleepRecord(document_id, start_time=None, end_time=None, sleep_rating=None):

    doc = sleep_record_ref.document('document_id')
    
    sleep_dict = dict()
    sleep_dict['start_time'] = start_time
    sleep_dict['end_time'] = end_time
    sleep_dict['sleep_rating'] = sleep_rating
    sleep_dict['last_updated'] = firestore.SERVER_TIMESTAMP
    
    doc.update(sleep_dict)

    return 


def deleteSleepRecord(document_id):
    
    doc = sleep_record_ref.document(document_id).delete()

    return "Done"
