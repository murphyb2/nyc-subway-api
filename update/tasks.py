from __future__ import absolute_import, unicode_literals

from celery import shared_task
from datetime import timedelta
from api.data.shouldUpdate import shouldUpdate
from api.data.importCSV import importCSV
from api.data.update import updateValues

@shared_task
def add(x,y):
    print(f'adding {x} and {y}')
    return x + y

@shared_task
def WeeklyUpdate():        
    upToDate = shouldUpdate()
    if "error" in upToDate:
        return {'success': False, 'error': upToDate["error"]}

    if(upToDate["shouldUpdate"] == False):
        return {'success': True, 'message': "All records are up to date"}
    
    print("db most recent saturday: " + upToDate["dbMostRecentSaturday"].strftime("%Y-%m-%d"))
    print("current saturday: " + upToDate["currentSaturday"].strftime("%Y-%m-%d"))

    saturdayToImport = upToDate["dbMostRecentSaturday"] + timedelta(days=7) 
    currentSaturday = upToDate["currentSaturday"]

    # download and import new weekly data
    while(saturdayToImport <= currentSaturday):
        result = importCSV(DATE=saturdayToImport.strftime("%y%m%d"))
        if(result['success'] == False):
            content = {
                'success': result['success'],
                'error': result['error']
            }
            return content
        saturdayToImport = saturdayToImport + timedelta(days=7)  

    # update net values
    result = updateValues(beginDate = upToDate["dbMostRecentSaturday"])
    content = {
        'success': result['success'],
        'msg': result['newMostRecentSaturday'],
        'error': result['error']
    }

    return content
