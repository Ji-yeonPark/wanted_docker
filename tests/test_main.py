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


def test_search_tag(client):
    """ 태그 검색 """

    # (한글)단어 검색
    response = client.get('/company/tag/?tag=태그_12')
    result = json.loads(response.data.decode())
    assert len(result) == 6

    # (일어)단어 검색
    response = client.get('/company/tag/?tag=タグ_')
    result = json.loads(response.data.decode())
    assert len(result) > 0


def test_add_tags_to_company(client):
    """ 회사에 태그 추가 """
    url = '/company/tag/'
    response = client.post(url, json={'tag': 17, 'company': 3})
    assert response.status_code == 201


def test_delete_tags_to_company(client):
    """ 회사 태그 삭제 """

    # 없는 태그 삭제
    url = '/company/tag/'
    response = client.delete(url, json={'tag': 17, 'company': 3})
    assert response.status_code == 404

    # 있는 태그 삭제
    response = client.delete(url, json={'tag': 1, 'company': 3})
    assert response.status_code == 200
