var SAInfo = {}

SAInfo.requestSelectData = function(self, selectDom, item, value) {
  var typeInfo = item.typeInfo
  var ajaxInfo = typeInfo.ajaxInfo
  ajaxInfo.success = function(ret) {
    var data = typeInfo.dataGenerator(ret)
    for (var i in data) {
      var it = data[i]
      var option = $('<option></option>')
      $(option).val(it.value).text(it.text)
      if (typeInfo.many) {
        for (var i in value) {
          if (it.value == value[i]) {
            $(option).attr('selected', 'selected')
            break
          }
        }
      } else {
        if (value && it.value == value) {
          $(option).attr('selected', 'selected')
        }
      }
      $(selectDom).append(option)
    }
    var responseHandler = typeInfo.responseHandler
    if (responseHandler) {
      responseHandler(self, selectDom, item, ret, value)
    }
  }
  $.ajax(ajaxInfo)
}

SAInfo.Boolean = function(self, item, value) {
  var getDom = SATable.getDom
  var div = getDom.Div('col-xs-12')

  var p = $('<p></p>')
  if (value == true) {
    $(p).addClass('text-success').append(getDom.IconYes())
  } else if (value == false) {
    $(p).addClass('text-danger').append(getDom.IconNo())
  } else {
    $(p).addClass('text-muted').append(getDom.IconQuestion())
  }

  var inputGroup = getDom.Div('input-group')
  var spanBtn = getDom.Span('input-group-btn')
  var select = $('<select class="form-control" name="'+item.name+'"></select>')
  var btn = getDom.Button('保存')
  $(btn).attr('type', 'submit')
  $(inputGroup).append(select).append(spanBtn)
  $(spanBtn).append(btn)

  var optionNone = $('<option></option>')
  var optionTrue = $('<option></option>')
  var optionFalse = $('<option></option>')
  $(optionNone).val(null).text('--')
  $(optionTrue).val(true).text('是')
  $(optionFalse).val(false).text('否')
  $(select).append(optionNone).append(optionTrue).append(optionFalse)
  if (value == true) {
    $(optionTrue).attr('selected', 'selected')
  } else if (value == false) {
    $(optionFalse).attr('selected', 'selected')
  } else {
    $(optionNone).attr('selected', 'selected')
  }

  var aEdit = $(item.dom.divEdit).find('a')
  if (item.typeInfo && item.typeInfo.writeOnly) {
    $(p).hide()
    $(aEdit).hide()
  } else {
    $(inputGroup).hide()
    $(aEdit).click(function() {
      if ($(inputGroup).is(':hidden')) {
        $(inputGroup).show()
        $(p).hide()
      } else {
        $(inputGroup).hide()
        $(p).show()
      }
    })
  }

  div.append(p).append(inputGroup)

  return div
}
SAInfo.Select = function(self, item, value) {
  var getDom = SATable.getDom
  var div = getDom.Div('col-xs-12')

  var typeInfo = item.typeInfo

  var p = $('<p></p>')
  if (typeInfo.many) {
    for (var i in value) {
      $(p).append(value[i]).append(getDom.Br())
    }
  } else {
    $(p).text(value)
  }

  var inputGroup = getDom.Div('input-group');
  var spanBtn = getDom.Span('input-group-btn');
  var select = $('<select class="form-control" name="'+item.name+'"></select>');
  var btn = getDom.Button('保存');
  $(btn).attr('type', 'submit');
  $(inputGroup).append(select).append(spanBtn);
  $(spanBtn).append(btn);

  if (typeInfo.many) {
    $(select).attr('multiple', 'multiple')
  }
  if (typeInfo.ajax) {
    SAInfo.requestSelectData(self, select, item, value)
  } else {
    var data = typeInfo.choices;
    for (var i in data) {
      var it = data[i]
      var option = $('<option></option>')
      $(option).val(it.value).text(it.text)
      if (typeInfo.many) {
        for (var i in value) {
          if (it.value == value[i]) {
            $(option).attr('selected', 'selected')
            break
          }
        }
      } else {
        if (value && it.value == value) {
          $(option).attr('selected', 'selected')
          $(p).text(it.text)
        }
      }
      $(select).append(option)
    }
  }

  var aEdit = $(item.dom.divEdit).find('a')
  if (item.typeInfo && item.typeInfo.writeOnly) {
    $(p).hide()
    $(aEdit).hide()
  } else {
    $(inputGroup).hide()
    $(aEdit).click(function() {
      if ($(inputGroup).is(':hidden')) {
        $(inputGroup).show()
        $(p).hide()
      } else {
        $(inputGroup).hide()
        $(p).show()
      }
    })
  }

  div.append(p).append(inputGroup)

  return div
}
SAInfo.Number = function(self, item, value) {
  var getDom = SATable.getDom

  var div = getDom.Div('col-xs-12')

  var p = $('<p></p>')
  $(p).text(value)

  var inputGroup = getDom.Div('input-group')
  var spanBtn = getDom.Span('input-group-btn')
  var input = getDom.Input(item.name)
  var btn = getDom.Button('保存')
  $(btn).attr('type', 'submit')
  $(inputGroup).append(input).append(spanBtn)
  $(spanBtn).append(btn)
  $(input).attr('type', 'number').val(value)

  var aEdit = $(item.dom.divEdit).find('a')
  if (item.typeInfo && item.typeInfo.writeOnly) {
    $(p).hide()
    $(aEdit).hide()
  } else {
    $(inputGroup).hide()
    $(aEdit).click(function() {
      if ($(inputGroup).is(':hidden')) {
        $(inputGroup).show()
        $(p).hide()
      } else {
        $(inputGroup).hide()
        $(p).show()
      }
    })
  }

  div.append(p).append(inputGroup)

  return div
}
SAInfo.Text = function(self, item, value) {
  var getDom = SATable.getDom
  var div = getDom.Div('col-xs-12')
  var typeInfo = item.typeInfo
  var ret = $('<p></p>')
  if (typeInfo && typeInfo.article) {
    var pre = $('<pre></pre>')
    $(pre).append(value)
    $(ret).append(pre)
  } else if (typeInfo && typeInfo.code) {
    var code = $('<code></code>')
    $(code).append(value)
    $(ret).append(code)
  } else if (typeInfo && typeInfo.markdown) {
    ret = $(markdown.toHTML(value))
  } else if(typeInfo && typeInfo.link && value !== null ){
    var a = $("<a></a>")
    var url = value
    var n1=url.indexOf("http://");
    var n2=url.indexOf("https://");
    if(n1 == -1 && n2 == -1)
    {
      url = "http://" + url
    }
    a.attr("href", url)
    a.attr("target","_blank")
    a.append(value)
    $(ret).append(a)
  }
  else {
    $(ret).append(value)
  }

  var inputGroup = getDom.Div('input-group')
  var inputGroup2 = getDom.Div('input-group')
  var spanBtn = getDom.Span('input-group-btn')
  var input = null

  if (typeInfo && (typeInfo.article || typeInfo.code || typeInfo.markdown || (!typeInfo.max_length))) {
    input = $('<textarea></textarea>')
    $(input).addClass('form-control').attr('name', item.name)
  } else {
    input = getDom.Input(item.name, item.caption)
    if (typeInfo && typeInfo.password) {
      $(input).attr('type', 'password')
      if (typeInfo.confirm) {
        var input2 = $(input).clone(true)
        $(input2).attr('name', item.name+'Confirm')
        $(input2).attr('placeholder', '请确认'+item.caption)
        $(inputGroup2).append(input2)
      }
    } else if (typeInfo && typeInfo.email) {
      $(input).attr('type', 'email')
    }
  }

  var btn = getDom.Button('保存')
  $(btn).attr('type', 'submit')
  $(inputGroup).append(input).append(spanBtn)
  $(spanBtn).append(btn)
  $(input).val(value)

  var aEdit = $(item.dom.divEdit).find('a')
  if (item.typeInfo && item.typeInfo.writeOnly) {
    $(ret).hide()
    $(aEdit).hide()
  } else {
    $(inputGroup).hide()
    $(aEdit).click(function() {
      if ($(inputGroup).is(':hidden')) {
        $(inputGroup).show()
        $(ret).hide()
      } else {
        $(inputGroup).hide()
        $(ret).show()
      }
    })
  }

  $(div).append(ret).append(inputGroup)

  if (typeInfo && typeInfo.password && typeInfo.confirm) {
    $(div).append(inputGroup2)
  }

  return div
}
SAInfo.Date = function(self, item, value) {
  /*var getDom = SATable.getDom
  var div = getDom.Div('col-xs-12')
  var typeInfo = item.typeInfo
  var ret = $('<p></p>')
  var date = new Date(value)
  var dateStr = date.toLocaleDateString()
  $(ret).append(dateStr)

  var inputGroup = getDom.Div('input-group')
  var inputGroup2 = getDom.Div('input-group')
  var spanBtn = getDom.Span('input-group-btn')
  var input = getDom.Input(item.name, item.caption)
  $(input).attr('readonly', 'readonly').datetimepicker({
      format: 'yyyy-mm-dd',
      minview: 2,
      maxview: 2,
     // weekStart: 1,
     //    todayBtn:  1,
		// autoclose: 1,
		// todayHighlight: 1,
		// startView: 2,
		// forceParse: 0,
     //    showMeridian: 1
  })

  var btn = getDom.Button('保存')
  $(btn).attr('type', 'submit')
  $(inputGroup).append(input).append(spanBtn)
  $(spanBtn).append(btn)
  $(input).val(value)

  var aEdit = $(item.dom.divEdit).find('a')
  if (item.typeInfo && item.typeInfo.writeOnly) {
    $(ret).hide()
    $(aEdit).hide()
  } else {
    $(inputGroup).hide()
    $(aEdit).click(function() {
      if ($(inputGroup).is(':hidden')) {
        $(inputGroup).show()
        $(ret).hide()
      } else {
        $(inputGroup).hide()
        $(ret).show()
      }
    })
  }

  $(div).append(ret).append(inputGroup)

  if (typeInfo && typeInfo.password && typeInfo.confirm) {
    $(div).append(inputGroup2)
  }

  return div*/
  var getDom = SATable.getDom
  var div = getDom.Div('col-xs-12')
  var typeInfo = item.typeInfo
  var ret = $('<p></p>')
  var date = new Date(value)
  var dateStr = date.toLocaleDateString()
  $(ret).append(dateStr);

  var inputGroup = getDom.Div('input-group')
  var inputGroup2 = getDom.Div('input-group')
  var spanBtn = getDom.Span('input-group-btn')
  var input = getDom.Input(item.name, item.caption)
  $(input).attr('readonly', 'readonly').datetimepicker({
     format: 'yyyy-mm-dd',
    minView: 2,
    maxView: 4
  })

  var btn = getDom.Button('保存')
  $(btn).attr('type', 'submit')
  $(inputGroup).append(input).append(spanBtn)
  $(spanBtn).append(btn)
  $(input).val(value)

  var aEdit = $(item.dom.divEdit).find('a')
  if (item.typeInfo && item.typeInfo.writeOnly) {
    $(ret).hide()
    $(aEdit).hide()
  } else {
    $(inputGroup).hide()
    $(aEdit).click(function() {
      if ($(inputGroup).is(':hidden')) {
        $(inputGroup).show()
        $(ret).hide()
      } else {
        $(inputGroup).hide()
        $(ret).show()
      }
    })
  }

  $(div).append(ret).append(inputGroup)

  if (typeInfo && typeInfo.password && typeInfo.confirm) {
    $(div).append(inputGroup2)
  }

  return div
}

SAInfo.Datetime = function(self, item, value) {
  // 目前仅支持只读
  var date = new Date(value)
  var dateStr = date.toLocaleString()
  var p = $('<p></p>')
  p.append(dateStr)
  return p
}
SAInfo.File = function(self, item, value) {
  // 目前仅支持写入
  var getDom = SATable.getDom
  var div = getDom.Div('col-xs-12')
  var typeInfo = item.typeInfo

  var inputGroup = getDom.Div('input-group')
  var spanBtn = getDom.Span('input-group-btn')
  var input = getDom.Input(item.name)
  $(input).attr('type', 'file')

  var btn = getDom.Button('保存')
  $(btn).attr('type', 'submit')
  $(inputGroup).append(input).append(spanBtn)
  $(spanBtn).append(btn)
  $(input).val(value)

  var aEdit = $(item.dom.divEdit).find('a')
  $(aEdit).hide()

  div.append(inputGroup)

  return div
}
SAInfo.Item = function(self, item, value) {
  typeInfo = item.typeInfo
  if (value) {
    value = value[typeInfo.field]
    var temItem = {
      name: item.name,
      caption: item.caption,
      readOnly: true,
      type: typeInfo.type,
      typeInfo: typeInfo.typeInfo,
      dom: item.dom
    }
    return SAInfo.itemTypeDom[typeInfo.type](self, temItem, value)
  } else {
    return $('<p></p>')
  }
}

SAInfo.itemTypeDom = {
  Boolean: SAInfo.Boolean,
  Number: SAInfo.Number,
  Text: SAInfo.Text,
  Date: SAInfo.Date,
  Datetime: SAInfo.Datetime,
  File: SAInfo.File,
  Select: SAInfo.Select,
  Item: SAInfo.Item
}

SAInfo.initData = function(self, info) {
  self.info = {}
  self.dom = {}

  self.info.gotoAttr = info.gotoButton;

  self.info.id = info.id
  self.info.title = info.title ? info.title : null
  self.info.getAttr = info.getURL ? { method: (info.getMethod ? info.getMethod.toUpperCase() : 'GET'), url: info.getURL } : null
  self.info.updateAttr = info.updateURL ? { method: (info.updateMethod ? info.updateMethod.toUpperCase( ) : 'POST'), url: info.updateURL } : null
  self.info.removeAttr = info.removeURL ? {
    method: (info.removeMethod ? info.removeMethod.toUpperCase( ) : 'POST'),
    url: info.removeURL,
    to: (info.removeToURL ? info.removeToURL : null)
  } : null
  self.info.items = info.items ? info.items : []
  self.info.errorMessage = {  //错误信息采用覆盖策略。传入的自定义信息会覆盖默认的处理文本。
      400: {
        head: '错误的访问', text: '发送了错误的请求信息。', showData: true
      },
      401: {
        head: '未认证', text: '请进行用户认证。', showData: false
      },
      403: {
        head: '访问被拒绝', text: '您位于不具备访问权限的用户组。', showData: false
      },
      404: {
        head: '访问失败', text: '请求的信息未找到。', showData: false
      },
      500: {
        head: '服务器错误', text: '服务器遇到了未料到到的情况。', showData: false
      },
      'else': {
        head: '发生错误', text: '发生错误。见详细信息。', showData: true
      }
  };
  if(info.errorMessage){
    for(var em in info.errorMessage)self.info.errorMessage[em] = info.errorMessage[em];
  }
  self.info.errorCustomField = info.errorCustomField ? info.errorCustomField : 'cause';
  self.info.errorCustom = info.errorCustom ? info.errorCustom : { }; //来自406的错误信息与其他错误信息分开管理。
}

SAInfo.POST = function(ajaxInfo, form, toURL, saInfo) {
  var data = SATable.getFormData(form)
  $.ajax({
    type: ajaxInfo.method,
    url: ajaxInfo.url,
    dataType: (ajaxInfo.dataType ? ajaxInfo.dataType : 'json' ),
    data: data,
    success: function(ret) {
      alert('成功！')
      location.reload()
    }
  })
}

SAInfo.SPECIAL = function(ajaxInfo, form, toURL, saInfo) {
  var contentType = false;
  var data = new FormData(form[0])

  if (saInfo) {
    var items = saInfo.info.items
    for (var i in items) {
      var it = items[i]
      if (it.type == 'Select' && it.typeInfo && it.typeInfo.many) {
        if (!data.has(it.name)) {
          data.set(it.name, [])
        }
      }
    }
  }

  $.ajax({
    url: ajaxInfo.url,
    method: ajaxInfo.method,
    data: data,
    contentType: contentType,
    processData: false,
    dataType: (ajaxInfo.dataType ? ajaxInfo.dataType : 'json' ),
    success: function(ret) {
      alert('成功！')
      if (toURL) {
        location.href = toURL
      } else {
        location.reload()
      }
    },
    error: function(info, x, xx) {
      var data = info.responseJSON;
      if(data){
        var response = "错误:\n";
        for(var i in data){
          response += "\n" + i + ": " + JSON.stringify(data[i]) + "\n";
        }
        alert(response);
      }else alert(info.responseText)
    }
  })
}

SAInfo.ajaxMethod = {
  POST: SAInfo.POST,
  PUT: SAInfo.SPECIAL,
  PATCH: SAInfo.SPECIAL,
  DELETE: SAInfo.SPECIAL
}

SAInfo.initInfo = function(self) {
  var info = self.info
  var dom = self.dom

  var getDom = SATable.getDom

  var divLoading = getDom.Div('row justify-content-sm-center jumbotron bg-faded')
  var divLoadingContent = getDom.Div('col-1')
  var iconLoading = getDom.IconLoading()
  $(divLoading).append(divLoadingContent)
  $(divLoadingContent).append(iconLoading)
  dom.divLoading = divLoading

  var divError = getDom.Div('column justify-content-sm-center jumbotron bg-faded');

  dom.divError = divError;

  var divContainer = getDom.Container()
  var divHead = getDom.RowBetween()
  dom.divContainer = divContainer
  dom.divHead = divHead
  if (info.title) {
    var divH2 = getDom.Div('col-md-7 col-sm-8')
    var h2 = getDom.H2(info.title)
    dom.divH2 = divH2
    dom.h2Title = h2
      $(divH2).append(h2)


    $(divHead).append(divH2)
  }
  if(info.gotoAttr){
    var spanGoto = getDom.Span();
    var gotoBtn = getDom.Button('');
    var formGoto = getDom.Form('');
    dom.btnGoto = gotoBtn;
    $(gotoBtn).append(getDom.IconNext());
    $(spanGoto).append(gotoBtn);
    $(formGoto).append(spanGoto);
    $(divHead).append(formGoto);

    if(info.gotoAttr.tooltip)
      $(gotoBtn).attr("data-toggle","tooltip").attr("title", info.gotoAttr.tooltip);

    if(info.gotoAttr.url)
      $(gotoBtn).click(function () {
        window.location = info.gotoAttr.url
      });
  }


  if (info.removeAttr) {
    var spanRemove = getDom.Span()
    var removeBtn = getDom.Button('')
    var formRemove = getDom.Form('')
    dom.btnRemove = removeBtn
    $(removeBtn).append(getDom.IconDelete())
    $(removeBtn).removeClass('btn-primary').addClass('btn-danger')
    $(spanRemove).append(removeBtn)
    $(formRemove).append(spanRemove)
    $(divHead).append(formRemove)

    $(removeBtn).click(function() {
      if (confirm("一旦删除将不可恢复，确认删除吗？")) {
        SAInfo.ajaxMethod[info.removeAttr.method](info.removeAttr, form, info.removeAttr.to)
      }
    })
  }
  $(divContainer).append(divHead).append(getDom.Br())

  var form = getDom.Form()
  var divInfo = getDom.Div()
  dom.divInfo = divInfo
  $(form).append(divInfo)
  $(divContainer).append(form)

  var items = info.items
  for (var i in items) {
    var item = items[i]
    if (item == 'Divide') {
      $(divInfo).append('<hr>')
    } else {
      self.initItem(self, item)
    }
  }

  $(form).submit(function() {
    var dataCheck = SATable.getFormData(form)
    var ok = true
    for (var i in items) {
      var item = items[i]
      if (item.typeInfo && item.typeInfo.confirm) {
        var value = dataCheck[item.name]
        var confirm = dataCheck[item.name+'Confirm']
        if (value != confirm) {
          ok = false
          alert(item.caption + '验证失败')
          break
        }
      }
    }

    if (ok) {
      SAInfo.ajaxMethod[info.updateAttr.method](info.updateAttr, form, null, self)
    }
  })

  $(divContainer).hide()
  $(divError).hide()
  $('#' + info.id).append(divLoading).append(divContainer).append(divError)
}

SAInfo.initItem = function(self, item) {
  var getDom = SATable.getDom
  var divInfo = self.dom.divInfo

  var divRow = getDom.Row()

  var divCaption = getDom.Div('col-lg-3 col-md-4 col-xs-11')
  var divEdit = getDom.Div('col-1')
  var divValue = getDom.Div('col-lg-8 col-md-7')
  $(divRow).append(divCaption).append(divValue).append(divEdit)

  var label = getDom.Label()
  var b = $('<b></b>')
  $(b).append(item.caption ? item.caption : item.name)
  $(divCaption).append(b)

  if ((!item.readOnly) && self.info.updateAttr) {
    var iconEdit = getDom.IconEdit()
    var a = getDom.A('', 'javascript:void(0)', 'text-info')
    $(a).append(iconEdit)
    $(divEdit).append(a)
  }

  $(divInfo).append(divRow)

  var dom = { divCaption: divCaption, divEdit: divEdit, divValue: divValue }
  item.dom = dom
}

SAInfo.fillInfo = function(self, item, value) {
  var divValue = item.dom.divValue
  var itemTypeDom = SAInfo.itemTypeDom

  if (itemTypeDom[item.type]) {
    $(divValue).empty().append(itemTypeDom[item.type](self, item, value))
  } else {
    $(divValue).empty().append(value)
  }
}

SAInfo.fillError = function (self, status, data) {
  var content = "";
  var customFunction = function (causeText) {
    var c = "<b><div>访问被禁止</div></b>\n";
    c += "<div>" + causeText + "</div>";
    return c;
  };
  var standardFunction = function (title, text, data) {
    var c = "<div><strong>" + title + "</strong></div>\n";
    c += "<div>" + text + "</div>\n";
    if(data){
      c += "<hr/><div><pre>\n";
      for(var i in data){
        c += i + ": " + JSON.stringify(data[i]) + "\n\n";
      }
      c += "</pre></div>";
    }
    return c;
  }
  if(status == 406){ // 特别错误状态。
    var customField = data[self.info.errorCustomField];
    if(customField){  // 目标字段被找到
      var causeText = self.info.errorCustom[customField];  // 查询对应的语法。
      if(!causeText){ // 没找到，试图找到else标记作为缺省。
        causeText = self.info.errorCustom['else']; // 默认以此作为else标记。
      }
      if(causeText){
        content = customFunction(causeText);
      }else { // 无论如何都找不到。还是采用标准输出。
        content = standardFunction("发生错误", "请求不可用。" ,data);
      }
    }else{  // 没有找到目标字段。采用标准错误输出。
      content = standardFunction("发生错误", "请求不可用。", data);
    }
  }else{  // 标准错误状态。
    var message = self.info.errorMessage[status];
    if(!message)message = self.info.errorMessage['else'];
    content = standardFunction(message.head, message.text, message.showData ? data : null);
  }
  self.dom.divError.html(content);
};

SAInfo.requestInfo = function(self) {
  var getAttr = self.info.getAttr
  $.ajax({
    method: getAttr.method,
    url: getAttr.url,
    dataType: 'json',
    success: function(ret) {
      self.dom.divContainer.show()
      self.dom.divLoading.hide()

      var items = self.info.items
      for (var i in items) {
        var item = items[i]
        if (item != 'Divide') {
          if (item.typeInfo && item.typeInfo.writeOnly) {
            self.fillInfo(self, item, null)
          }
          self.fillInfo(self, item, ret[item.name])
        }
      }
    },error: function (ret) {
        self.dom.divLoading.hide();
        self.dom.divError.show();
        var data = ret.responseJSON;
        self.fillError(self, ret.status, data);
      }
  })
}

SATable.SimpleAjaxInfo = function(info) {
  var saInfo = {
    initData: SAInfo.initData,
    initInfo: SAInfo.initInfo,
    initItem: SAInfo.initItem,
    requestInfo: SAInfo.requestInfo,
    fillInfo: SAInfo.fillInfo,
    fillError: SAInfo.fillError,
  }
  saInfo.initData(saInfo, info)
  saInfo.initInfo(saInfo)
  saInfo.requestInfo(saInfo)

}