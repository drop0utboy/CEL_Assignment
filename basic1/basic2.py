import time
import os
import pandas as pd
import numpy as np
import math

'''
   01 
   폴더명을 입력하면 폴더에 저장되어 있는 csv 파일들의 상대경로를 리스트 타입으로 반환함  

        Parameters:
            pathname (str): 데이터 파일이 들어있는 폴더명
                            데이터 이름은 날짜_vehicle.csv 으로 구성됨
                            단, 해당 폴더에는 여러 csv파일들이 존재할 수 있고 csv파일이 아닌 다른 파일들은 무시함
                            파일명 예시 - 20200804_vehicle.csv

        Returns:
            file_path_list (str): 폴더에 들어있는 csv 파일들의 상대경로를 반환 
                                  값은 날짜를 기반으로 정렬되어 반환된다. 
            
            ['dataset/20200804_vehicle.csv', 'dataset/20200805_vehicle.csv', 'dataset/20200806_vehicle.csv', 'dataset/20200807_vehicle.csv']

        Examples:
            >>> load_filenames("dataset")[:2]
            ['dataset/20200804_vehicle.csv', 'dataset/20200805_vehicle.csv']

    '''

def load_filenames(pathname):
    file_list = []

    #_vehicle.csv로 끝나는 파일만을 리스트에 담기
    for filename in os.listdir(pathname):
        if filename.endswith('_vehicle.csv'):
            #반환되는 값의 \\를 /으로 변경경
            temp_01 = os.path.join(pathname, filename)
            file_list.append(temp_01.replace('\\','/'))

    # / 로 나눠 앞의 숫자 값을 비교해서 sort
    file_list.sort(key=lambda x: x.split('/')[-1])
    
    #정렬된 리스트 반환
    return file_list

# Debug
# print(load_filenames('dataset'))





'''
    02
    상대경로가 저장된 리스트 타입을 입력하면, 해당 파일들로부터 데이터를 읽어 날짜별로 리스트를 생성하고,
    이들을 다시 하나의 리스트에 저장하여 반환하는 함수

        Parameters:
            filepath_list (list): 여러 파일들의 상대경로. 리스트 형태로 저장되어 있음
                                  리스트 예시 - ['dataset/20200804_vehicle.csv', 'dataset/20200805_vehicle.csv',
                                                 'dataset/20200806_vehicle.csv', 'dataset/20200807_vehicle.csv']

        Returns:
            dataset_list (list): 날짜별로 차량의 이동 데이터가 저장된 리스트

        Examples:
            >>> dataset_list = load_dataset_from_files(filepath_list)
            >>> dataset_list[0][:3]
                [['9848769553', 158.694108, 65.86921, '20200804_132818'],
                ['F3718E8F31', 158.70332, 65.874825, '20200804_132909'],
                ['9AC8C9DEFF', 158.70654299999995, 65.866976, '20200804_132941']]
            >>> len(dataset_list)
                4

    '''


def load_dataset_from_files(filepath_list):
    dataset_list = []
    for filepath in filepath_list:
        dataset_list.append(pd.read_csv(f'{filepath}').values.tolist())

    # len 체크
    # print(len(dataset_list))

    return dataset_list

# #debug
# filepath_list = load_filenames('dataset')

# load_dataset_from_files(filepath_list)




'''
    03
    삼중 중첩된 리스트 형태로 되어 있는 데이터를 이중 중첩된 리스트형태로 변환하는 함수

        Parameters:
            dataset_list (list): 날짜별로 차량의 이동 데이터가 저장된 삼중 중첩 리스트 
        Returns:
            merged_dataset (list): 날짜 구분 없이 차량의 이동 데이터가 저장된 이중 중첩 리스트

        Examples:
            >>> dataset_list = load_dataset_from_files(filepath_list)
            >>> merged_dataset = concat_all_dataset(dataset_list)
            >>> len(merged_dataset)
                15859
            >>> merged_dataset[-3:]                 
                [['3265535978', 158.712142, 65.868156, '20200807_235944'],
                 ['5FE301A05D', 158.717659, 65.87973199999999, '20200807_235945'],
                 ['5FE301A05D', 158.717659, 65.87974, '20200807_235955']]

    '''

def concat_all_dataset(dataset_list):
    merged_dataset = [data for day_data in dataset_list for data in day_data]
    
    # #debug
    # print(merged_dataset[-5:])

    return merged_dataset


# #debug

# dataset_list = load_dataset_from_files(filepath_list)

# concat_all_dataset(dataset_list)




'''
    04
    위도와 경도를 가진 두 개의 GPS 데이터를 리스트형 데이터로 입력하면 두 점 사이의 거리를 계산하여 반환한다.
    두 점 사이의 거리는 Euclidean 거리로 계산된다.
            
        Parameters:
            v1_gps (list): 첫 번째 GPS 지점의 위치, [gps_lon, gps_lat]로 구성됨 
            v2_gps (list): 두 번째 GPS 지점의 위치, [gps_lon, gps_lat]로 구성됨 
    
        Returns:
            distance (float): 두 지점 사이의 거리를 floating point로 표현함    
    
        Examples:
            >>> v1 = [158.694108, 65.86921]
            >>> v2 = [158.70332, 65.874825]
            >>> mv.get_distance(v1, v2)
                0.010788381203864588
    '''






def get_distance(v1_gps, v2_gps):

    distance = 0
    
    #위도차
    lon_dif = v2_gps[0] - v1_gps[0]
    #경도차
    lat_dif = v2_gps[1] - v1_gps[1]

    distance = (lon_dif**2 + lat_dif**2)**0.5

    # #debug
    # print(distance)

    return distance



# # debug
# v1_gps = [dataset_list[0][0][1], dataset_list[0][0][2]]
# v2_gps = [dataset_list[0][1][1], dataset_list[0][1][2]]

# print(v1_gps, v2_gps)


# get_distance(v1_gps, v2_gps)




'''
    05 
    모든 데이터가 통합된 merged_dataset을 입력받고 시간대 별로 각 차량의 평균 위치를 계산하는 함수.
    각 차량의 시간당 위치의 평균은 해당 시간대에 있는 모든 GPS 위도/경도의 평균값을 취한다. 
    즉, gps_lon과 gps_lat의 각각의 평균값을 시간별로 계산할 수 있다.
    시간대는 마지막 column에 있는 timestamp 값을 내림하면 된다. 
    예를 들면, '20200807_235944'은 '20200807_230000' 으로 변환한다.
    
        Parameters:
            merged_dataset (list): 날짜 구분 없이 차량의 이동 데이터가 저장된 이중 중첩 리스트         
    
        Returns:
            average_location_per_hour (dict): 시간대별로 각 차량의 평균 위치가 저장된 dict 타입의 변수
                                              여기서 시간대가 dict 타입의 key값으로 존재한다.
                                                    
        Examples:
            >>> dataset_list = load_dataset_from_files(filepath_list)
            >>> merged_dataset = concat_all_dataset(dataset_list)
            >>> get_average_location_per_hour(merged_dataset)
                {'20200804_130000': [['08B40E9C2A', 158.703385, 65.874044],
                                     ['0EA2E922A4', 158.709489, 65.86888400000001],
                                     ['147914D9E1', 158.705941, 65.87392600000001],
                                     ['16D9353696', 158.697445, 65.87181799999999]
                                     ....
    '''


def get_average_location_per_hour(merged_dataset):
    df = pd.DataFrame(merged_dataset)
    df.columns = ['blk_key', 'gps_lon', 'gps_lat', 'timestamp']

    # 시간대 데이터 추가가
    df['hour'] = df['timestamp'].str[:11] + '0000'

    # 그룹화 및 평균치로 압축
    grouped = df.groupby(['hour', 'blk_key'], as_index=False).agg({
            'gps_lon': 'mean',
            'gps_lat': 'mean'
        })

    # 딕셔너리화
    average_location_per_hour = {}
    for index, row in grouped.iterrows():
        hour = row['hour']
        blk_key = row['blk_key']
        avg_lon = row['gps_lon']
        avg_lat = row['gps_lat']

        # 내부 딕셔너리 초기화
        if hour not in average_location_per_hour:
            average_location_per_hour[hour] = []

        average_location_per_hour[hour].append([blk_key, avg_lon, avg_lat])

        
    return average_location_per_hour

# #debug
# get_average_location_per_hour(merged_dataset)


#처음엔 단순히 딕셔너리에서 값을 하나씩 꺼내서 비교하는 식으로 for 문으로 풀려고 했으나 복잡해서 데이터프레임으로 해결


'''
    06
    각 시간대 별로 가장 가까이 위치하는 차량 쌍을 추출하고 이때의 거리를 반환하는 함수
        
        Parameters:
            average_location_per_hour (dict): 시간대별로 각 차량의 평균 위치가 저장된 변수
        
        Returns:
            vehicle_shortest_distance_dict (dict): 시간대별로 가장 가까이 위치하는 차량 쌍과 그 거리가 저장된 변수
                                                   여기서 시간대가 dict 타입의 key값으로 존재한다.
                                                    
        Examples:
            >>> dataset_list = load_dataset_from_files(filepath_list)
            >>> merged_dataset = concat_all_dataset(dataset_list)
            >>> average_location_per_hour = get_average_location_per_hour(merged_dataset)
            >>> get_vehicle_list_having_shortest_distance(average_location_per_hour)
                {'20200804_130000': ['51A00423A8', '9A258A3200', 6.499999999221018e-05],
                 '20200804_140000': ['8279CD2AB8', '9C59F673A7', 8.374365648500866e-05],
                 '20200804_150000': ['51A00423A8', '9A258A3200', 6.499999999221018e-05],
                 '20200804_160000': ['8279CD2AB8', '9C59F673A7', 8.374365648500866e-05],
                 '20200804_170000': ['51A00423A8', '9A258A3200', 6.499999999221018e-05],
                 ...
    '''

# 유클리드 거리로 비교한 함수
def get_vehicle_list_having_shortest_distance (average_location_per_hour):
    vehicle_shortest_distance_dict = {}

    # 시간대별 정리
    for hour, vehicles in average_location_per_hour.items():
        shortest_distance = float('inf')
        closest_cars = []

        # 가장 가까운 차량 쌍 찾기
        for i in range(len(vehicles)):
            for j in range(i+1, len(vehicles)):
                car1 = vehicles[i]
                car2 = vehicles[j]

                # 위도경도 
                lat_1, lon_1 = car1[2], car1[1]
                lat_2, lon_2 = car2[2], car2[1]

                # 거리 계산
                distance = (lat_2 - lat_1) ** 2 + (lon_2 - lon_1) ** 2

                # 가장 가까운 차량 쌍 ID
                if distance < shortest_distance:
                    shortest_distance = distance
                    closest_cars = [car1[0], car2[0]]


        # 딕셔너리에 저장
        if closest_cars:
            vehicle_shortest_distance_dict[hour] = [closest_cars[0], closest_cars[1], shortest_distance]
    
    return vehicle_shortest_distance_dict


# # debug
# average_location_per_hour = get_average_location_per_hour(merged_dataset)

# get_vehicle_list_having_shortest_distance (average_location_per_hour)


# 하버사인 거리 함수를 이용해서 계산
# 하버사인 거리 함수
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # 지구 반지름 (km)
    
    # 위도, 경도를 라디안으로 변환
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # 위도, 경도의 차이 계산
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # 하버사인 공식 적용
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # 거리 계산
    distance = R * c  # 단위: km
    return distance



# 하버사인 공식 함수를 이용한 함수
def get_vehicle_list_having_shortest_distance (average_location_per_hour):
    vehicle_shortest_distance_dict = {}

    # 시간대별 정리
    for hour, vehicles in average_location_per_hour.items():
        shortest_distance = float('inf')
        closest_cars = []

        # 가장 가까운 차량 쌍 찾기
        for i in range(len(vehicles)):
            for j in range(i+1, len(vehicles)):
                car1 = vehicles[i]
                car2 = vehicles[j]

                # 위도경도 
                lat_1, lon_1 = car1[2], car1[1]
                lat_2, lon_2 = car2[2], car2[1]

                # 거리 계산 하버사인 공식 사용
                distance = haversine(lat_1, lon_1, lat_2, lon_2)

                # 가장 가까운 차량 쌍 ID
                if distance < shortest_distance:
                    shortest_distance = distance
                    closest_cars = [car1[0], car2[0]]


        # 딕셔너리에 저장
        if closest_cars:
            vehicle_shortest_distance_dict[hour] = [closest_cars[0], closest_cars[1], shortest_distance]
    
    return vehicle_shortest_distance_dict


# # debug
# average_location_per_hour = get_average_location_per_hour(merged_dataset)

# get_vehicle_list_having_shortest_distance (average_location_per_hour)



'''
    07
    날짜별 모든 차량이 주행한 거리의 총합을 계산하는 함수
    '''


def total_traveled_distance(merged_dataset):
    total_distance = 0
    total_distance_per_day = {}

    df = pd.DataFrame(merged_dataset)
    df.columns = ['blk_key', 'gps_lon', 'gps_lat', 'timestamp']
    df['days'] = df['timestamp'].str[:8]

    # 날짜와 차량 ID로 정렬렬
    df = df.sort_values(by=['blk_key', 'days'])

    for vehicle, vehicle_data in df.groupby('blk_key'):
        previous_row = None

        # 차량별로 연속된 위치 간의 거리 계산
        for index, row in vehicle_data.iterrows():
            if previous_row is not None:
                # 유클리드 거리 계산 (위도, 경도)
                lat1, lon1 = previous_row['gps_lat'], previous_row['gps_lon']
                lat2, lon2 = row['gps_lat'], row['gps_lon']

                distance = (lat2 - lat1) ** 2 + (lon2 - lon1) ** 2

                # 날짜별 총 주행 거리 합산
                day = row['days']
                if day not in total_distance_per_day:
                    total_distance_per_day[day] = 0
                total_distance_per_day[day] += distance

            previous_row = row

    return total_distance_per_day

# # debug
# total_traveled_distance(merged_dataset)


# 이전의 평균 구하던 함수의 응용



'''
08 
날짜별 모든 차량이 주행한 시간의 총합을 계산하는 함수
'''


def total_traveled_time(merged_dataset):
    total_time_per_day = {}

    df = pd.DataFrame(merged_dataset)
    df.columns = ['blk_key', 'gps_lon', 'gps_lat', 'timestamp']
    df['days'] = df['timestamp'].str[:8]

    # 날짜와 차량 ID로 정렬
    df = df.sort_values(by=['blk_key', 'days'])

    for vehicle, vehicle_data in df.groupby('blk_key'):
        previous_row = None

        # 차량별로 연속된 위치 간의 시간 차이 계산
        for index, row in vehicle_data.iterrows():
            if previous_row is not None:
                # 주행 시간 차이 계산산
                timestamp1 = previous_row['timestamp']
                timestamp2 = row['timestamp']
                
                # datetime으로 변환
                time1 = pd.to_datetime(timestamp1, format='%Y%m%d_%H%M%S')
                time2 = pd.to_datetime(timestamp2, format='%Y%m%d_%H%M%S')
                
                # 시간 차이 계산 (초)
                time_diff = (time2 - time1).total_seconds()

                # 날짜별 총 주행 시간 합산
                day = row['days']
                if day not in total_time_per_day:
                    total_time_per_day[day] = 0
                total_time_per_day[day] += time_diff

            previous_row = row

    # 결과 반환
    return total_time_per_day

# # debug
# total_traveled_time(merged_dataset)




if __name__ == "__main__":    
    
    DATA_PATH = "dataset"

    start_tm = time.time()
    filepath_list = load_filenames(DATA_PATH)
    dataset_list = load_dataset_from_files(filepath_list)
    merged_dataset = concat_all_dataset(dataset_list)
    average_location_per_hour = get_average_location_per_hour(merged_dataset)
    vehicle_shortest_distance_dict = get_vehicle_list_having_shortest_distance(average_location_per_hour)

    total_shortest_distance = sum([value[-1] for key, value in vehicle_shortest_distance_dict.items()])
    print(f"각 시간별 vehicle 최단거리의 합 : {total_shortest_distance}")
    """
    total_traveled_distance()와 total_traveled_time() 함수는 각각 날짜별 모든 차량이 주행한 거리의 총합과 시간의 총합을 계산하는 함수입니다.
    함수명과 리턴값은 지키되 함수의 파라미터 등 코드 구현은 자유롭게 하시면 됩니다.
    """
    # 날짜별 모든 차량이 주행한 거리의 총합
    total_traveled_distance_value = total_traveled_distance(merged_dataset)
    print(f"날짜별 모든 차량이 주행한 거리의 총합 : {total_traveled_distance_value}")

    # 날짜별 모든 차량이 주행한 시간의 총합
    total_traveled_time_value = total_traveled_time(merged_dataset)   
    print(f"날짜별 모든 차량이 주행한 시간의 총합 : {total_traveled_time_value}")
    end_tm = time.time()
    print(f"실행시간 : {end_tm - start_tm}")