import glob
import os
import datetime
import codecs

def get_recently_modified_files(directory_path, num_files=8):
    # 디렉토리에서 가장 최근에 수정된 파일들을 가져옴
    files = glob.glob(os.path.join(directory_path, '*.html'))
    files.sort(key=os.path.getmtime, reverse=True)
    
    # 최근에 수정된 num_files개의 파일을 반환
    return files[:num_files]

def map_weekday_to_index(date, start_weekday=0):
    weekday = date.weekday()
    mapped_weekday = (weekday - start_weekday) % 7
    return mapped_weekday

def get_weekday_mapping(recent_files, start_weekday=0):
    weekday_mapping = []
    for file in recent_files:
        # 파일명에서 year, month, day 추출
        date_str = file[-15:-5]
        year = int(date_str[:4])
        month = int(date_str[5:7])
        day = int(date_str[8:])
        
        # 날짜에 해당하는 요일 매핑
        date = datetime.date(year, month, day)
        mapped_weekday = map_weekday_to_index(date, start_weekday)
        
        weekday_mapping.append(mapped_weekday)
    
    return weekday_mapping

directory_path = "C:/Nexon/TalesWeaver/ChatLog/" #@@@@@@@@@@@@@@@@@님 채팅로그 위치를 넣으세요
recent_files = get_recently_modified_files(directory_path, num_files=8)
weekday_mapping = get_weekday_mapping(recent_files, start_weekday=0)
print(recent_files)
print(weekday_mapping)
i = 0

#요일 바뀜 제거 - 닉네임 확인을 위함.
if weekday_mapping.count(6) == 2:
    lastweek = recent_files[7]
    del recent_files[7]
    del weekday_mapping[7]
else: # 일요일이 - 1개 일때
    for k in range (8):
       if weekday_mapping[k] == 6:
           lastweek = recent_files[k]
           break

print(lastweek)
#이후 요일 제거
while i < len(weekday_mapping) - 1:
    if weekday_mapping[i] < weekday_mapping[i+1]:
        del recent_files[i+1]
        del weekday_mapping[i+1]
    else:
        i += 1
        
recent_files.reverse()
weekday_mapping.reverse()
print(recent_files)
print(weekday_mapping)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

filter_file_path = './filter1.txt'
nickname_list = [''] #@@@@@@@@@@@@@@@@@@@@@@@@@@ 님 닉네임 추가해야함
filter_list_True=['점수', '입장'] 
filter_list_False=['사용','지불','TP'] # 필터 추가 예정
previous_nickname = None
current_nickname = None

with codecs.open(lastweek, 'r', 'euc-kr', errors='ignore') as html_file:
    for line in html_file:
        if '<font size="2" color="#ff64ff">' in line:
            if any(keyword in line for keyword in filter_list_True) or any(nickname in line for nickname in nickname_list):
                for nickname in nickname_list:
                    if nickname in line:
                        previous_nickname = nickname
                        current_nickname = previous_nickname
                if not any(f_keyword in line for f_keyword in filter_list_False):
                    # 필터링된 텍스트를 추가하지 않음
                    pass
                    # 필요한 작업 수행
                        
#파일 초기화 : 수정요일과 로그의 날짜가 다를때 (추가예정)                        
with open(filter_file_path, 'w') as filter_file:
    filter_file.write('')

with open(filter_file_path, 'a') as filter_file:
        filter_file.write(f"\n[[이전 닉네임 {previous_nickname}]]\n")

    

for file_path in recent_files:
    # 파일 경로에서 파일 이름 추출
    file_name = os.path.basename(file_path)
    
    # 파일명에 해당하는 요일 매핑 인덱스 가져오기
    index = recent_files.index(file_path)
    mapped_weekday = weekday_mapping[index]
    
    # 파일명과 날짜, 요일 매핑을 추가
    with open(filter_file_path, 'a') as filter_file:
        filter_file.write(f"\n---------------[[ 날짜 : {file_name[-15:-5]} 요일 : {mapped_weekday} ]]---------------------------------------------\n\n")

                        
     # 파일을 EUC-KR로 인코딩하여 읽기
    with codecs.open(file_path, 'r', 'euc-kr', errors='ignore') as html_file:
        for line in html_file:
            if '<font size="2" color="#ff64ff">' in line:
                if any(keyword in line for keyword in filter_list_True) or any(nickname in line for nickname in nickname_list):
                    # 현재 닉네임 원소 추출
                    for nickname in nickname_list:
                        if nickname in line:
                            current_nickname = nickname
                            break

                    # 이전 닉네임 원소와 비교하여 다른 경우에 '\n 닉네임이 다릅니다 \n' 표기
                    if current_nickname != None and previous_nickname != None:
                        if current_nickname != previous_nickname:
                            with open(filter_file_path, 'a') as filter_file:
                                filter_file.write(f'\n---------------닉네임이 다릅니다------------------\n[[이전 닉네임: {previous_nickname} 현재 닉네임: {current_nickname}]]\n\n')


                    # filtered_line 생성
                    filtered_line = line[30:44]+ line[83:-14] + '\n'

                    # filter_file_path에 저장
                    with open(filter_file_path, 'a') as filter_file:
                        filter_file.write(filtered_line)

                    # 이전 닉네임 원소 업데이트
                    previous_nickname = current_nickname

                            
    
