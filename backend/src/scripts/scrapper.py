import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_ppp_members():
    # 지역구: PGB006
    # 비례대표: PGB007
    url = "https://www.peoplepowerparty.kr/about/people_partisan/PGB007"
    members_data = []
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        info_elements = soup.find_all(class_='info')
        print(f"총 {len(info_elements)}명의 의원 정보를 수집합니다...")
        
        for info in info_elements:
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
            
            member_info = {
                '이름': name,
                '지역구': district,
                '생년월일': birth_date,
                '전화번호': phone,
                '이메일': email,
                '홈페이지': homepage
            }
            
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
    df = scrape_ppp_members()