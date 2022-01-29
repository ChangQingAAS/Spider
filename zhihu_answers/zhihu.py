import requests, json
import datetime
import pandas as pd
from selectolax.parser import HTMLParser

question = '如何看待演员吴京发文支持动画电影《雄狮少年》？'
question_id = 507372651

url = 'https://www.zhihu.com/api/v4/questions/%s/answers' % question_id
headers = {
    'Host': 'www.zhihu.com',
    'user-agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'referer': 'https://www.zhihu.com/question/%s' % question_id
}
df = pd.DataFrame(columns=('author', 'fans_count', 'content', 'created_time',
                           'updated_time', 'comment_count', 'voteup_count',
                           'url'))


def crawler(start):
    print(start)
    global df
    data = {
        'include':
        'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_recognized;data[*].mark_infos[*].url;data[*].author.follower_count,vip_info,badge[*].topics;data[*].settings.table_of_content.enabled',
        'offset': start,
        'limit': 20,
        'sort_by': 'default',
        'platform': 'desktop'
    }

    #将携带的参数传给params
    r = requests.get(url, params=data, headers=headers)
    res = json.loads(r.text)
    if res['data']:
        for answer in res['data']:
            author = answer['author']['name']
            fans = answer['author']['follower_count']
            content = HTMLParser(answer['content']).text()
            #content = answer['content']
            created_time = datetime.datetime.fromtimestamp(
                answer['created_time'])
            updated_time = datetime.datetime.fromtimestamp(
                answer['updated_time'])
            comment = answer['comment_count']
            voteup = answer['voteup_count']
            link = answer['url']

            row = {
                'author': [author],
                'fans_count': [fans],
                'content': [content],
                'created_time': [created_time],
                'updated_time': [updated_time],
                'comment_count': [comment],
                'voteup_count': [voteup],
                'url': [link]
            }
            df = df.append(pd.DataFrame(row), ignore_index=True)

        if len(res['data']) == 20:
            crawler(start + 20)
    else:
        print(res)


crawler(0)
df.to_csv(f'./zhihu_answers/%s.csv' % question, index=False)
print("done~")