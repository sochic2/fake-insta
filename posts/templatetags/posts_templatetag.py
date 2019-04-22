#폴더만들기, 파일 두개 만들기 ==> 필터만들 준비 완료
from django import template

register = template.Library()

@register.filter
def hashtag_link(post):
    content = post.content+' '
    hashtags = post.hashtags.all()
    
    # hashtags를 순회하면서, content 내에서 
    #해당 문자열(해시태그)를 링크를 포함한 문자열로 치환한다.
    for hashtag in hashtags:
        content = content.replace(hashtag.content+' ', "<a href = '/posts/hashtag/%d'>%s</a> " %(hashtag.pk, hashtag.content))
    return content