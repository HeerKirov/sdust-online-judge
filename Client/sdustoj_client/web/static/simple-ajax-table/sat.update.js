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

  var inputGroup = getDom.Div('input-group')
  var spanBtn = getDom.Span('input-group-btn')
  var select = $('<select class="form-control" name="'+item.name+'"></select>')
  var btn = getDom.Button('保存')
  $(btn).attr('type', 'submit')
  $(inputGroup).append(select).append(spanBtn)
  $(spanBtn).append(btn)

  if (typeInfo.many) {
    $(select).attr('multiple', 'multiple')
  }
  if (typeInfo.ajax) {
    SAInfo.requestSelectData(self, select, item, value)
  } else {
    var data = typeInfo.choices
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
  } else if(typeInfo && typeInfo.link ){
    var a = $("<a></a>")
    var url = value
    var n=url.indexOf("https://")
    if(n == -1)
    {
      url = "https://" + url
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
  var getDom = SATable.getDom
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
     weekStart: 1,
        todayBtn:  1,
		autoclose: 1,
		todayHighlight: 1,
		startView: 2,
		forceParse: 0,
        showMeridian: 1
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
      alert(info.responseText)
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
      if (confirm("一旦删除将不可恢复，确认码？")) {
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
  $('#' + info.id).append(divLoading).append(divContainer)
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
    }
  })
}

SATable.SimpleAjaxInfo = function(info) {
  var saInfo = {
    initData: SAInfo.initData,
    initInfo: SAInfo.initInfo,
    initItem: SAInfo.initItem,
    requestInfo: SAInfo.requestInfo,
    fillInfo: SAInfo.fillInfo
  }
  saInfo.initData(saInfo, info)
  saInfo.initInfo(saInfo)
  saInfo.requestInfo(saInfo)

}