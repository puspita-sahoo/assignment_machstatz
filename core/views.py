import re
import json
import requests
from datetime import datetime,timedelta

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def ping(request):
    return JsonResponse({'message': 'pong'})

@csrf_exempt
def production_count(request):
    # INPUT
    input_data = json.loads(request.body)

    q_start_time = datetime.strptime(input_data['start_time'],"%Y-%m-%dT%H:%M:%SZ")
    q_end_time = datetime.strptime(input_data['end_time'],"%Y-%m-%dT%H:%M:%SZ")

    response = requests.get('https://gitlab.com/-/snippets/2094509/raw/master/sample_json_1.json')
    data = response.json()
    
    monitor = {
        "shiftA":{ # 6am - 14(2pm) | 8hrs
            "production_A_count" :0,
            "production_B_count" :0
        },
        "shiftB":{ # 14(2pm) - 20(8pm) | 8hrs
            "production_A_count" :0,
            "production_B_count" :0
        },
        "shiftC":{ # 20(8pm) - 6am | 10hrs
            "production_A_count" :0,
            "production_B_count" :0
        }
    }

    for i in data:
        production_status_time = datetime.strptime(i['time'], '%Y-%m-%d %H:%M:%S')
        if q_start_time < production_status_time < q_end_time:
            if 6 < production_status_time.hour < 14:
                if i['production_A']:
                    monitor["shiftA"]['production_A_count'] +=1
                if i['production_B']:
                    monitor["shiftA"]['production_B_count'] +=1
            elif 14 < production_status_time.hour < 20:
                if i['production_A']:
                    monitor["shiftB"]['production_A_count'] +=1
                if i['production_B']:
                    monitor["shiftB"]['production_B_count'] +=1
            else:
                if i['production_A']:
                    monitor["shiftC"]['production_A_count'] +=1
                if i['production_B']:
                    monitor["shiftC"]['production_B_count'] +=1
    return JsonResponse(monitor)

@csrf_exempt
def machine_data(request):
    # INPUT
    input_data = json.loads(request.body)

    q_start_time = datetime.strptime(input_data['start_time'],"%Y-%m-%dT%H:%M:%SZ")
    q_end_time = datetime.strptime(input_data['end_time'],"%Y-%m-%dT%H:%M:%SZ")

    response = requests.get("https://gitlab.com/-/snippets/2094509/raw/master/sample_json_2.json")
    data = response.json()

    runtime = 0
    downtime = 0

    for i in data:
        machine_status_time = datetime.strptime(i['time'], "%Y-%m-%d %H:%M:%S")
        if q_start_time < machine_status_time < q_end_time:
            if i['runtime'] > 1021:
                extra_downtime = i['runtime'] - 1021
                runtime += 1021
                downtime += i['downtime'] + extra_downtime
            else:
                runtime += i['runtime']
                downtime += i['downtime']

    return JsonResponse({
        "runtime": f"{runtime//3600}h:{runtime%3600//60}m:{runtime%60}s",
        "downtime": f"{downtime//3600}h:{downtime%3600//60}m:{downtime%60}s",
        "utilisation": (runtime) / (runtime + downtime) * 100
    })

@csrf_exempt
def belts_avg(request):
    # INPUT
    input_data = json.loads(request.body)

    q_start_time = datetime.strptime(input_data['start_time'],"%Y-%m-%dT%H:%M:%SZ")
    q_end_time = datetime.strptime(input_data['end_time'],"%Y-%m-%dT%H:%M:%SZ")

    response = requests.get("https://gitlab.com/-/snippets/2094509/raw/master/sample_json_3.json")
    api_data = response.json()

    master_data = {}

    for data in api_data:
        time =  datetime.strptime(data['time'],"%Y-%m-%d %H:%M:%S")
        if q_start_time < time < q_end_time : 
            id = int(re.findall(r'\d+', data['id'])[0])
            if id in master_data:
                master_data[id]["belt1_values"].append(0 if data['state'] else data['belt1'])
                master_data[id]["belt2_values"].append(0 if not data['state'] else data['belt2'])
            else:
                master_data[id] = {
                    "belt1_values" : [ 0 if data['state'] else data['belt1']],
                    "belt2_values" : [ 0 if not data['state'] else data['belt2']]
                }
    final_data = []
    for id, data in master_data.items():

        final_data.append({
            "id": id,
            "avg_belt1" : round(sum(data['belt1_values'])/len(data['belt1_values'])),
            "avg_belt2" : round(sum(data['belt1_values'])/len(data['belt1_values'])),
        })

    return JsonResponse(final_data, safe=False)










