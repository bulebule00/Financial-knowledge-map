from django.shortcuts import render
from toolkit.pre_load import pre_load_thu
from toolkit.NER import get_NE, temporaryok, get_explain, get_detail_explain

def Begin_to_identify(request):  # index页面需要一开始就加载的内容写在这里
    context = {}
    ctx = {}
    if request.POST:
        key = request.POST["user_text"]
        thu1 = pre_load_thu
        # 使用thulac进行分词 TagList[i][0]代表第i个词
        # TagList[i][1]代表第i个词的词性
        key = key.strip()
        TagList = thu1.cut(key, text=False)#[[词，词性], [词，词性], []]
        text = ""
        NE_List = get_NE(key)  # 获取实体列表

        for pair in NE_List:  # 根据实体列表，显示各个实体
            if pair[1] == 0:
                text += pair[0]
                continue
            if temporaryok(pair[1]):  # 判断实体词性
                # text += "<a href='#'  data-original-title='" + get_explain(
                #     pair[1]
                # ) + "(暂无资料)'  data-placement='top' data-trigger='hover' data-content='" + get_detail_explain(pair[1]) + "' class='popovers'>" + pair[0] + "</a>"

                # continue
                text += "<a href='#'  data-original-title='" + pair[1]+ "(暂无资料)'  data-placement='top' data-trigger='hover' data-content='" + pair[1] + "' class='popovers'>" + pair[0] + "</a>"
                continue

                # text += "<a href='detail.html?title=" + pair[0] + "'  data-original-title='" + get_explain(
                #     pair[1]) + "'  data-placement='top' data-trigger='hover' data-content='" + get_detail_explain(pair[1]) + "' class='popovers'>" + pair[0] + "</a>"
            # "http://stockdata.stock.hexun.com/gszl/s000001.shtml"

            text += "<a href='http://stockdata.stock.hexun.com/gszl/s"+str(pair[1])+".shtml'>"+str(pair[0])+"</a>"
            # text += "<a href='http://stockdata.stock.hexun.com/gszl/s"+str(pair[1])+".shtml'>"+str(pair[0])+"</a>"

            # text += "<a href='detail.html?title=" + pair[0] + "'  data-original-title='" +pair[1]+"'  data-placement='top' data-trigger='hover' data-content='" + pair[1]+ "' class='popovers'>" + pair[0] + "</a>"
            # <a href="detail.html?title=平安银行   data-original-title=类别 data-placement="top" data-trigger="hover" data-content="类别描述" class="popovers" ">平安银行<a>
            #   跳转链接，  应该只是跳转个链接带个titile,  这些属性应该是在<a>标签之上的。

        ctx['rlt'] = text  # 将实体对应类别和描述，+ 对应单词放入ctx字典，以key=rlt进行查询

        seg_word = ""
        length = len(TagList)  # TagList分词后的数量
        for t in TagList:  # 测试打印词性序列
            seg_word += t[0] + " <strong><small>[" + t[1] + "]</small></strong> "  # 将单词和词向进行添加标签
        seg_word += ""  # 后面加入""
        ctx['seg_word'] = seg_word  # 以seg_word的key进行查询

    return  render(request, "index.html", ctx)#返回主页面