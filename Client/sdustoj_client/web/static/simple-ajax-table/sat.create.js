var SAForm = {}

SAForm.Boolean = function(self, item) {
  var options = []
  if (item.defaultTrue) {
    options = [
      { text: '是', value: 'true', selected: true },
      { text: '否', value: 'false' },
    ]
  } else {
    options = [
      { text: '是', value: 'true' },
      { text: '否', value: 'false', selected: true },
    ]
  }
  return SATable.getDom.InputSelect(item.name, item.caption, options)
}
SAForm.Text = function(self, item) {
  var getDom = SATable.getDom
  var typeInfo = item.typeInfo

  var div = getDom.Div('form-group row')
  var label = $('<label class="col-md-3 col-form-label">' + item.caption + '</label>')
  var divInput = SATable.getDom.Div('col-md-9')
  var input
  if (typeInfo && typeInfo.max_length) {
    input = getDom.Input(item.name, '')
    $(input).attr('maxlength', typeInfo.max_length)
  } else {
    input = $('<textarea></textarea>')
    $(input).addClass('form-control').attr('name', item.name)
  }

  $(div).append(label).append(divInput)
  $(divInput).append(input)

  return div
}

SAForm.Date = function(self, item) {
  var getDom = SATable.getDom
  var typeInfo = item.typeInfo

  var div = getDom.Div('form-group row')
  var label = $('<label class="col-md-3 col-form-label">' + item.caption + '</label>')
  var divInput = SATable.getDom.Div('col-md-9 input-append date form_datetime')
  var input = getDom.Input(item.name, '')
  $(input).attr('readonly', 'readonly').datetimepicker({
     weekStart: 1,
        todayBtn:  1,
		autoclose: 1,
		todayHighlight: 1,
		startView: 2,
		forceParse: 0,
        showMeridian: 1
  })


  $(div).append(label).append(divInput)
  $(divInput).append(input)

  return div
}

SAForm.Select = function(self, item) {
  var typeInfo = item.typeInfo
  var options = typeInfo.options ? typeInfo.options : []
  var input = SATable.getDom.InputSelect(item.name, item.caption, options)
  var select = $(input).find('select')
  if (typeInfo.many) {
    $(select).attr('multiple', 'multiple')
  }
  if (typeInfo.ajax) {
    SAForm.requestSelectData(self, select, item)
  } else {
    var data = typeInfo.choices
    for (var i in data) {
      var it = data[i]
      var option = $('<option></option>')
      $(option).attr('value', it.value).text(it.text)
      $(select).append(option)
    }
  }

  return input
}
SAForm.Number = function(self, item) {
  var getDom = SATable.getDom
  var typeInfo = item.typeInfo

  var div = getDom.Div('form-group row')
  var label = $('<label class="col-md-3 col-form-label">' + item.caption + '</label>')
  var divInput = SATable.getDom.Div('col-md-9')
  var input = getDom.Input(item.name, '')

  $(input).attr('type', 'number')

  $(div).append(label).append(divInput)
  $(divInput).append(input)

  return div
}
SAForm.Email = function(self, item) {
  var getDom = SATable.getDom
  var typeInfo = item.typeInfo

  var div = getDom.Div('form-group row')
  var label = $('<label class="col-md-3 col-form-label">' + item.caption + '</label>')
  var divInput = SATable.getDom.Div('col-md-9')
  var input = getDom.Input(item.name, '')

  $(input).attr('type', 'email')
  if (typeInfo.max_length) {
    input.attr('max_length', typeInfo.max_length)
  }

  $(div).append(label).append(divInput)
  $(divInput).append(input)

  return div
}
SAForm.Password = function(self, item) {
  var getDom = SATable.getDom
  var typeInfo = item.typeInfo

  var div = getDom.Div('form-group row')
  var label = $('<label class="col-md-3 col-form-label">' + item.caption + '</label>')
  var divInput = SATable.getDom.Div('col-md-9')
  var input = getDom.Input(item.name, '')

  $(input).attr('type', 'password')
  if (typeInfo && typeInfo.max_length) {
    $(input).attr('maxlength', typeInfo.max_length)
  }

  $(div).append(label).append(divInput)
  $(divInput).append(input)

  if (typeInfo.confirm) {
    label = $('<label class="col-md-3 col-form-label">请确认</label>')
    divInput = SATable.getDom.Div('col-md-9')
    input = getDom.Input(item.name + 'Confirm', '')

    $(input).attr('type', 'password')

    if (typeInfo && typeInfo.max_length) {
      $(input).attr('maxlength', typeInfo.max_length)
    }

    $(div).append(getDom.Br()).append(getDom.Br()).append(label).append(divInput)
    $(divInput).append(input)
  }

  return div
}


SAForm.requestSelectData = function(self, selectDom, item) {
  var typeInfo = item.typeInfo
  var ajaxInfo = typeInfo.ajaxInfo
  ajaxInfo.success = function(ret) {
    var data = typeInfo.dataGenerator(ret)
    for (var i in data) {
      var it = data[i]
      var option = $('<option></option>')
      $(option).val(it.value).text(it.text)
      $(selectDom).append(option)
    }
    var responseHandler = typeInfo.responseHandler
    if (responseHandler) {
      responseHandler(self, selectDom, item, ret)
    }
  }
  $.ajax(ajaxInfo)
}

SAForm.inputDomChoice = {
  Boolean: SAForm.Boolean,
  Text: SAForm.Text,
  Date: SAForm.Date,
  Select: SAForm.Select,
  Number: SAForm.Number,
  Email: SAForm.Email,
  Password: SAForm.Password
}

SAForm.initData = function(self, formInfo) {
  self.formInfo = {}
  self.formInfo.id = formInfo.id
  self.formInfo.method = formInfo.method
  self.formInfo.url = formInfo.url
  self.formInfo.items = []
  self.formInfo.toSuccess = formInfo.toSuccess ? formInfo.toSuccess : null

  self.formDom = {}

  var items = formInfo.items
  var formItems = self.formInfo.items
  for (var i in items) {
    var it = items[i]
    var item = {}
    item.name = it.name
    item.caption = it.caption ? it.caption : it.name
    item.type = it.type ? it.type : 'Text'
    item.typeInfo = it.typeInfo ? it.typeInfo : {}
    if (it.defaultTrue) {
      item.defaultTrue = true
    }

    formItems.push(item)
  }
}

SAForm.initForm = function(self) {
  var formInfo = self.formInfo
  var getDom = SATable.getDom

  var divContainer = getDom.Container()
  var form = getDom.Form()
  var br = getDom.Br()
  var btnSubmit = getDom.ButtonSubmit('提 交')

  self.formDom.divContainer = divContainer
  self.formDom.form = form
  self.formDom.btnSubmit = btnSubmit

  $(divContainer).append(form)
  self.initItems(self)
  $(form).append(br).append(btnSubmit)

  $(btnSubmit).click(function() {
    $(form).submit()
  })
  $(form).submit(function() {
    var formData = SATable.getFormData(form)
    var valid = true

    var items = formInfo.items
    for (var it in items) {
      var info = items[it]
      if (info.typeInfo && info.typeInfo.confirm) {

        var value = formData[info.name]
        var confirm = formData[info.name + 'Confirm']
        if (value != confirm) {
          alert(info.caption + '两次输入不一致')
          valid = false
          $(self.formDom.btnSubmit).find('button').removeClass('btn-primary').addClass('btn-danger').text(info.caption + '两次输入不一致')
        }
      }
    }

    if (valid) {
      for (var i in formData) {
        if ((formData[i] instanceof Array) && formData[i].length == 0) {
          delete formData[i]
        }
      }

      $.ajax({
        type: formInfo.method,
        url: formInfo.url,
        data: formData,
        traditional: true,
        success: function(ret) {
          alert('成功！')
          if (formInfo.toSuccess) {
            location.href = formInfo.toSuccess
          }
        },
        error: function(info, message, errorObj) {
          self.setError(self, info, message, errorObj)
        }
      })

    }
  })

  $('#' + formInfo.id).append(divContainer)
}

SAForm.initItems = function(self) {
  var formInfo = self.formInfo
  var formDom = self.formDom
  var items = formInfo.items
  var form = formDom.form
  for (var i in items) {
    var item = items[i]
    if (SAForm.inputDomChoice[item.type]) {
      var dom = SAForm.inputDomChoice[item.type](self, item)
      form.append(dom)
    }
  }
}

SAForm.setError = function(self, errorInfo, errorMessage, errorObj) {
  alert(errorInfo.responseText)
  var text = '提交'
  if (errorInfo.status == '400') {
    text = '所填内容错误'
  } else if (errorInfo.status = '403') {
    text = '拒绝访问'
  } else if (errorInfo.status = '500') {
    text = '服务器错误'
  } else {
    text = '网络错误'
  }
  $(self.formDom.btnSubmit).find('button').removeClass('btn-primary').addClass('btn-danger').text(text)
}

SATable.SimpleAjaxForm = function(formInfo) {
  var ajaxForm = {
    initData: SAForm.initData,
    initForm: SAForm.initForm,
    initItems: SAForm.initItems,
    setError: SAForm.setError
  }
  ajaxForm.initData(ajaxForm, formInfo)
  ajaxForm.initForm(ajaxForm)
  return ajaxForm
}