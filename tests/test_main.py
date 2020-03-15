import json


def test_search_company(client):
    # 전체 검색
    response = client.get('/company/')
    assert response.status_code == 200

    # (한글)단어 검색
    response = client.get('/company/?name=원')  # 원티드 1개 존재
    assert response.status_code == 200
    result = json.loads(response.data.decode())
    assert len(result) == 1

    # (영어)단어 검색
    response = client.get('/company/?name=dat')  # dat 포함하는 단어 2개 존재
    result = json.loads(response.data.decode())
    assert len(result) == 2

    # 없는 단어 검색
    response = client.get('/company/?name=가나다')
    result = json.loads(response.data.decode())
    assert len(result) == 0
