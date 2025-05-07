# -*- coding: utf-8 -*-
import requests

from src.config import GLOBAL_CONFIG
from src.utils import UA


def __login_req() -> requests.Response:
    return requests.post(f'{GLOBAL_CONFIG.bolo_config.host}/oauth/bolo/login', headers={'User-Agent': UA}, data={
        'username': GLOBAL_CONFIG.bolo_config.username,
        'password': GLOBAL_CONFIG.bolo_config.password
    })


def bolo_login() -> None:
    res = __login_req()
    if res.status_code != 200:
        print(f'登陆bolo失败: 请重新登陆 {res.text}')
        GLOBAL_CONFIG.bolo_config.username = ''
        GLOBAL_CONFIG.bolo_config.password = ''
        return

    GLOBAL_CONFIG.bolo_config.cookie = res.headers['Set-Cookie']
    print(f'bolo登陆成功 {GLOBAL_CONFIG.bolo_config.host} 用户 {
          GLOBAL_CONFIG.bolo_config.username}')


def push_article(article: dict) -> dict:
    while GLOBAL_CONFIG.bolo_config.cookie == '':
        while GLOBAL_CONFIG.bolo_config.username == '':
            print("请输入bolo用户名:")
            GLOBAL_CONFIG.bolo_config.username = input('')
        while GLOBAL_CONFIG.bolo_config.password == '':
            print("请输入bolo密码:")
            GLOBAL_CONFIG.bolo_config.password = input('')
        bolo_login()
    res = requests.post(f'{GLOBAL_CONFIG.bolo_config.host}/console/article/', headers={
        'User-Agent': UA,
        'Cookie': GLOBAL_CONFIG.bolo_config.cookie
    }, json={
        "article": {
            "articleTitle": article.articleTitle,
            "articleContent": article.articleOriginalContent,
            "articleAbstract": article.articlePreviewContent,
            "articleTags": article.articleTags,
            "articlePermalink": "",
            "articleStatus": 0,
            "articleSignId": "1",
            "postToCommunity": False,
            "articleCommentable": True,
            "articleViewPwd": "",
            "category": ""
        }
    })
    if res.status_code != 200:
        print(f'push帖子失败: {res.text}')
        return
    else:
        print('推送成功')
