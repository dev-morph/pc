from bs4 import BeautifulSoup
import requests
import json
import time
import re
import pandas as pd

def parse_member_detail(detail_text):
    print("의원 상세 정보를 파싱하여 학력/경력/수상 정보로 분류")
    result = {
        'education': [],
        'career': [],
        'awards': []
    }
    
    current_section = None
    lines = str(detail_text).split('<br/>')
    
    for line in lines:
        line = clean_text(line)
        if not line:
            continue
            
        lower_line = line.lower()
        if any(keyword in lower_line for keyword in ['학력', '학 력', 'education']):
            current_section = 'education'
            continue
        elif any(keyword in lower_line for keyword in ['경력', '주요경력', '경 력', 'career']):
            current_section = 'career'
            continue
        elif any(keyword in lower_line for keyword in ['수상', 'award']):
            current_section = 'awards'
            continue
            
        if current_section and line:
            line = line.lstrip('■●▲-○·※').strip()
            if line:
                result[current_section].append(line)
    
    return result

def clean_text(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_member_code(onclick_attr):
    match = re.search(r"peoplePartisanPop\('peoplePopup','([^']+)'\)", onclick_attr)
    if match:
        return match.group(1)
    return None

def extract_member_codes(thumb_element):
    # member_codes = []
    pattern = r"peoplePartisanPop\('peoplePopup','([^']+)'\)"
    result = None
    # for member in member_list:
    #     onclick = member.find('a')['onclick']
    #     match = re.search(pattern, onclick)
    #     if match:
    #         member_codes.append(match.group(1))
    onclick = thumb_element.find('a')['onclick']
    match = re.search(pattern, onclick)
    if match:
        return match.group(1)
    
    return result

def get_member_detail(member_code):
    print(f"의원 상세 정보를 수집합니다... {member_code}")
    detail_url = "https://www.peoplepowerparty.kr/about/people_partisan_detail?ppparty_csrf_name=cb3ecf86d2ad5db620295970e8aed6bf&mona_cd="
    detail_url += member_code
    response = requests.get(detail_url)
    time.sleep(1)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        name = soup.find('h3').text.strip()
        people_detail = soup.find(class_="people-detail")
        
        if people_detail:
            parsed_detail = parse_member_detail(people_detail)
            return {
                'name': name,
                'member_code': member_code,
                **parsed_detail
            }
    except Exception as e:
        print(f"[ERROR] {member_code} 의원 정보 파싱 중 오류 발생: {e}")
    
    return None


# def scrape_ppp_members_detail():
#     try:
#         # 메인 페이지 크롤링
#         # 지역구: PGB006
#         # 비례대표: PGB007
#         url = "https://www.peoplepowerparty.kr/about/people_partisan/PGB006"
#         detail_url = "https://www.peoplepowerparty.kr/about/people_partisan_detail?ppparty_csrf_name=cb3ecf86d2ad5db620295970e8aed6bf&mona_cd="
#         response = requests.get(url)
#         time.sleep(1)
#         soup = BeautifulSoup(response.text, 'html.parser')
        
#         members_data = []
#         member_list = soup.find_all(class_='thumb')
#         member_codes = extract_member_codes(member_list)
#         print(member_codes)
        
#         for member_code in member_codes:
#             detail_url += member_code
#             response = requests.get(detail_url)
#             time.sleep(1)
#             soup = BeautifulSoup(response.text, 'html.parser')
#             detail = get_member_detail(member_code)
#             print(detail)
#         return detail;
#     except Exception as e:
#         print(f"[ERROR] 처리 중 오류 발생: {e}")
#         return None

def scrape_ppp_members():
    # 지역구: PGB006
    # 비례대표: PGB007
    url = "https://www.peoplepowerparty.kr/about/people_partisan/PGB006"
    members_data = []
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        li_element = soup.find(class_='result-search').find_all("li")
        print(f"총 {len(li_element)}명의 의원 정보를 수집합니다...")

        for info in li_element:
            # 기본 정보 추출
            name = info.find('h3').text.strip()
            district = info.find('span').text.strip()
            
            # dd 태그 내의 정보 추출
            dd_row = info.find('dd', class_='row')
            p_tags = dd_row.find_all('p')
            
            # 생년월일, 전화, 이메일 추출
            birth_date = p_tags[0].text.replace('생년월일', '').strip()
            phone = p_tags[1].text.replace('전화', '').strip()
            email = p_tags[2].text.replace('이메일', '').strip()
            
            # SNS 정보 추출 (있는 경우에만)
            sns_div = info.find('div', class_='sns')
            homepage = ''
            if sns_div:
                homepage_link = sns_div.find('a', class_='home')
                if homepage_link:
                    homepage = homepage_link.get('href', '')
            
            thumb_element = info.find(class_='thumb')
            member_codes = extract_member_codes(thumb_element)
            detail = get_member_detail(member_codes)

            member_info = {
                '이름': name,
                '지역구': district,
                '생년월일': birth_date,
                '전화번호': phone,
                '이메일': email,
                '홈페이지': homepage,
                "member_code": member_codes,
                "education": detail.get('education', []),
                "career": detail.get('career', []),
                "awards": detail.get('awards', [])
            }
            
            print(member_info)
            members_data.append(member_info)
            
        # DataFrame 생성
        df = pd.DataFrame(members_data)
        
        # CSV 파일로 저장
        df.to_csv('ppp_members.csv', index=False, encoding='utf-8-sig')
        print(f"데이터 수집 완료! 총 {len(df)}명의 의원 정보를 저장했습니다.")
        
        # 데이터 미리보기 출력
        print("\n=== 데이터 미리보기 ===")
        print(df.head())
        
        return df
        
    except Exception as e:
        print(f"[ERROR] 처리 중 오류 발생: {e}")
        return None

if __name__ == "__main__":
    print("국민의힘 국회의원 정보 수집을 시작합니다.\n")
    members = scrape_ppp_members()