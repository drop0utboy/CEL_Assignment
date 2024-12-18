import time
def load_filenames(pathname):
    '''
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
    
    return None

def load_dataset_from_files(filepath_list):
    '''
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
    return None

def concat_all_dataset(dataset_list):
    '''
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
    return None

def get_distance(v1_gps, v2_gps):
    '''
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
    return None

def get_average_location_per_hour(merged_dataset):
    '''
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
    return None

def get_vehicle_list_having_shortest_distance (average_location_per_hour):
    '''
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
    return None


def total_traveled_distance():
    '''
    날짜별 모든 차량이 주행한 거리의 총합을 계산하는 함수
    '''
    return None

def total_traveled_time():
    '''
    날짜별 모든 차량이 주행한 시간의 총합을 계산하는 함수
    '''
    return None

if __name__ == "__main__":    
    
    DATA_PATH ="dataset"

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
    total_traveled_distance_value = total_traveled_distance()
    print(f"날짜별 모든 차량이 주행한 거리의 총합 : {total_traveled_distance_value}")

    # 날짜별 모든 차량이 주행한 시간의 총합
    total_traveled_time_value = total_traveled_time()   
    print(f"날짜별 모든 차량이 주행한 시간의 총합 : {total_traveled_time_value}")
    end_tm = time.time()
    print(f"실행시간 : {end_tm - start_tm}")