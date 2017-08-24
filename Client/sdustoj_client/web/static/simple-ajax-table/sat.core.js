var SATable = {}

SATable.getFormData = function(form) {
  var array = $(form).serializeArray()
  var data = {}
  for (var i in array) {
    var it = array[i]
    if (data[it.name]) {
      if (!(data[it.name] instanceof Array)) {
        var oldValue = data[it.name]
        data[it.name] = []
        data[it.name].push(oldValue)
      }
      data[it.name].push(it.value)
    } else {
      data[it.name] = it.value
    }
  }

  return data
}

SATable.getDom = {}
SATable.getDom.Br = function(class_) {
  var br = $('<br/>')
  if (class_) {
    $(br).addClass(class_)
  }
  return br
}
SATable.getDom.Div = function(class_) {
  var div = $('<div></div>')
  if (class_) {
    $(div).addClass(class_)
  }
  return div
}
SATable.getDom.Container = function(class_) {
  classes = 'container'
  if (class_) {
    classes += ' ' + class_
  }
  return SATable.getDom.Div(classes)
}
SATable.getDom.Row = function(class_) {
  classes = 'row'
  if (class_) {
    classes += ' ' + class_
  }
  return SATable.getDom.Div(classes)
}
SATable.getDom.RowBetween = function(class_) {
  classes = 'row justify-content-between'
  if (class_) {
    classes += ' ' + class_
  }
  return SATable.getDom.Div(classes)
}
SATable.getDom.BtnGroup = function(class_) {
  var div = SATable.getDom.Div('btn-group')
  $(div).attr('role', 'group')
  if (class_) {
    $(div).addClass(class_)
  }
  return div
}
SATable.getDom.H2 = function(text, class_) {
  var h2 = $('<h2></h2>')
  if (text) {
    $(h2).text(text)
  }
  if (class_) {
    $(h2).addClass(class_)
  }
  return h2
}
SATable.getDom.H3 = function(text, class_) {
  var h3 = $('<h3></h3>')
  if (text) {
    $(h3).text(text)
  }
  if (class_) {
    $(h3).addClass(class_)
  }
  return h3
}
SATable.getDom.ButtonOutline = function(name, class_) {
  var btn = $('<button type="button" class="btn btn-outline-primary"></button>')
  if (name) {
    $(btn).text(name)
  }
  if (class_) {
    $(btn).addClass(class_)
  }
  return btn
}
SATable.getDom.Button = function(name, class_) {
  var btn = $('<button type="button" class="btn btn-primary"></button>')
  if (name) {
    $(btn).text(name)
  }
  if (class_) {
    $(btn).addClass(class_)
  }
  return btn
}
SATable.getDom.ButtonSubmit = function(name) {
  var span = $('<span class="input-group-btn"></span>')
  var btn = SATable.getDom.Button(name)
  $(span).append(btn)
  return span
}
SATable.getDom.A = function(name, href, class_) {
  var a = $('<a></a>')
  if (name) {
    $(a).text(name)
  }
  if (href) {
    $(a).attr('href', href)
  }
  if (class_) {
    $(a).addClass(class_)
  }
  return a
}
SATable.getDom.AButton = function(name, href, class_) {
  var a = SATable.getDom.A(name, 'javascript:void(0)', 'btn btn-primary')
  if (href) {
    $(a).attr('href', href)
  }
  if (class_) {
    $(a).addClass(class_)
  }
  return a
}
SATable.getDom.Form = function(class_) {
  var form = $('<form class="form" onsubmit="return false;"></form>')
  if (class_) {
    form.addClass(class_)
  }
  return form
}
SATable.getDom.Span = function(class_) {
  var span = $('<span></span>')
  if (class_) {
    $(span).addClass(class_)
  }
  return span
}
SATable.getDom.Label = function(text, class_) {
  var label = $('<label></label>')
  if (text) {
    $(label).text(text)
  }
  if (class_) {
    $(label).addClass(class_)
  }
  return label
}
SATable.getDom.Input = function(name, placeholder, class_) {
  var input = $('<input type="text" class="form-control" name="'+name+'" placeholder="'+placeholder+'"/>')
  if (class_) {
    $(input).addClass(class_)
  }
  return input
}
SATable.getDom.InputText = function(name, caption, placeholder, class_) {
  var div = SATable.getDom.Div('form-group row')
  var label = $('<label class="col-md-3 col-form-label">' + caption + '</label>')
  var divInput = SATable.getDom.Div('col-md-9')
  var input = $('<input class="form-control" type="text" name="' + name + '"/>')
  if (placeholder) {
    $(input).attr('placeholder', placeholder)
  }
  $(divInput).append(input)
  $(div).append(label).append(divInput)
  if (class_) {
    $(div).addClass(class_)
  }

  return div
}
SATable.getDom.InputSelect = function(name, caption, options, class_) {
  var div = SATable.getDom.Div('form-group row')
  var label = $('<label class="col-md-3 col-form-label">' + caption + '</label>')
  var divInput = SATable.getDom.Div('col-md-9')
  var select = $('<select class="form-control">')
  if (name) {
    $(select).attr('name', name)
  }

  for (var i in options) {
    var it = options[i]
    var option = $('<option></option>')
    if (it.value) {
      $(option).val(it.value)
    }
    if (it.text) {
      $(option).text(it.text)
    }
    if (it.selected) {
      $(option).attr('selected', 'selected')
    }
    $(select).append(option)
  }

  $(divInput).append(select)
  $(div).append(label).append(divInput)
  if (class_) {
    $(div).addClass(class_)
  }

  return div
}
SATable.getDom.Nav = function(class_) {
  var nav = $('<nav></nav>')
  if (class_) {
    $(nav).addClass(class_)
  }
  return nav
}
SATable.getDom.Ul = function(class_) {
  var ul = $('<ul></ul>')
  if (class_) {
    $(ul).addClass(class_)
  }
  return ul
}
SATable.getDom.Li = function(class_) {
  var li = $('<li></li>')
  if (class_) {
    $(li).addClass(class_)
  }
  return li
}
SATable.getDom.Table = function(class_) {
  var table = $('<table class="table table-hover"></table>')
  if (class_) {
    $(table).addClass(class_)
  }
  return table
}
SATable.getDom.THead = function(class_) {
  var tHead = $('<thead></thead>')
  if (class_) {
    $(tHead).addClass(class_)
  }
  return tHead
}
SATable.getDom.TBody = function(class_) {
  var tBody = $('<tbody></tbody>')
  if (class_) {
    $(tBody).addClass(class_)
  }
  return tBody
}
SATable.getDom.Tr = function(class_) {
  var tr = $('<tr></tr>')
  if (class_) {
    $(tr).addClass(class_)
  }
  return tr
}
SATable.getDom.Td = function(class_) {
  var td = $('<td></td>')
  if (class_) {
    $(td).addClass(class_)
  }
  return td
}
SATable.getDom.Th = function(class_) {
  var th = $('<th></th>')
  if (class_) {
    $(th).addClass(class_)
  }
  return th
}
SATable.getDom.IconLoading = function(class_) {
  var icon = $('<i class="fa fa-circle-o-notch fa-spin fa-2x fa-fw"></i>')
  if (class_) {
    $(icon).addClass(class_)
  }
  return icon
}
SATable.getDom.IconDown = function(class_) {
  var icon = $('<i class="fa fa-chevron-circle-down fa-fw"></i>')
  if (class_) {
    $(icon).addClass(class_)
  }
  return icon
}
SATable.getDom.IconUp = function(class_) {
  var icon = $('<i class="fa fa-chevron-circle-up fa-fw"></i>')
  if (class_) {
    $(icon).addClass(class_)
  }
  return icon
}
SATable.getDom.IconLast = function(class_) {
  var icon = $('<i class="fa fa-angle-left"></i>')
  if (class_) {
    $(icon).addClass(class_)
  }
  return icon
}
SATable.getDom.IconNext = function(class_) {
  var icon = $('<i class="fa fa-angle-right"></i>')
  if (class_) {
    $(icon).addClass(class_)
  }
  return icon
}
SATable.getDom.IconNoDirection = function(class_) {
  var icon = $('<i class="fa fa-minus-circle fa-fw"></i>')
  if (class_) {
    $(icon).addClass(class_)
  }
  return icon
}
SATable.getDom.IconYes = function(class_) {
  var icon = $('<i class="fa fa-check fa-fw"></i>')
  if (class_) {
    $(icon).addClass(class_)
  }
  return icon
}
SATable.getDom.IconNo = function(class_) {
  var icon = $('<i class="fa fa-close fa-fw"></i>')
  if (class_) {
    $(icon).addClass(class_)
  }
  return icon
}
SATable.getDom.IconQuestion = function(class_) {
  var icon = $('<i class="fa fa-question fa-fw"></i>')
  if (class_) {
    $(icon).addClass(class_)
  }
  return icon
}
SATable.getDom.IconEdit = function(class_) {
  var icon = $('<i class="fa fa-pencil-square-o fa-fw"></i>')
  if (class_) {
    $(icon).addClass(class_)
  }
  return icon
}
SATable.getDom.IconDelete = function(class_) {
  var icon = $('<i class="fa fa-trash fa-fw"></i>')
  if (class_) {
    $(icon).addClass(class_)
  }
  return icon
}

SATable.types = {}
SATable.types.Boolean = function(content, column, info) {
  return content ? SATable.getDom.IconYes : SATable.getDom.IconNo
}
SATable.types.Datetime = function(content, column, info) {
  var date = new Date(content)
  return date.toLocaleString()
}
SATable.types.Date = function(content, column, info) {
  var date = new Date(content)
  return date.toLocaleDateString()
}
SATable.types.Link = function(content, column, info) {
  var typeInfo = column.typeInfo
  var url = typeInfo.base_url + info[typeInfo.key] + '/'
  return SATable.getDom.A(content, url)
}
SATable.types.Text = function(content, column, info) {
  return content
}

SATable.InputType = {
  'text': SATable.getDom.InputText
}

SATable.hasFilter = function() {
  return this.filters.length > 0
}

SATable.hasSearch = function() {
  return this.search
}

SATable.createFilterForm = function() {
  var self = this
  var getDom = SATable.getDom

  var divContainer = getDom.Container('jumbotron bg-faded collapse')
  var formFilter = getDom.Form()

  for (var i in self.filters) {
    var filter = self.filters[i]
    var input = SATable.InputType[filter.type](filter.name, filter.caption, filter.placeholder)
    $(formFilter).append(input)
  }

  var btnSubmit = getDom.ButtonSubmit('筛 选')

  $(formFilter).append(getDom.Br()).append(btnSubmit)
  $(divContainer).attr('id', self.tableIDs.filterDiv).append(formFilter)

  self.dom.filter.form = formFilter
  self.dom.filter.div = divContainer
  self.dom.filter.submit = btnSubmit

  $(btnSubmit).click(function() {
    self.update()
  })

  return divContainer
}

SATable.createHead = function() {
  var self = this
  var getDom = SATable.getDom

  var divBetween = getDom.RowBetween()

  var divTitle = getDom.Div()
  var h2Title = getDom.H2(self.title)
  var divBtn = getDom.BtnGroup()
  $(divTitle).addClass('col-6').append(h2Title)
  if (self.hasFilter()) {
    var btnFilter = getDom.ButtonOutline('筛选')
    $(btnFilter).attr('data-toggle', 'collapse').attr('data-target', '#' + self.tableIDs.filterDiv)
    $(divBtn).append(btnFilter)

    self.dom.filter.button = btnFilter
  }
  if (self.createURL != null) {
    var btnCreate = getDom.AButton('创建', self.createURL)
    $(divBtn).append(btnCreate)
  }
  $(divBetween).append(divTitle).append(divBtn)

  return divBetween
}

SATable.createBarUp = function() {
  var self = this
  var getDom = SATable.getDom

  var divBetween = getDom.RowBetween()
  var divSearch = getDom.Div('col-md-5 col-sm-12')
  var divPage = getDom.Div('col-md-6 col-sm-12')
  $(divBetween).append(divSearch).append(divPage)

  var nav = getDom.Nav()
  var ul = getDom.Ul('pagination ' + self.tableIDs.pageClass)
  $(nav).attr('style', 'float:right;').append(ul)
  $(divPage).append(nav)

  self.dom.pagination.up = {}
  self.dom.pagination.up.div = divPage
  self.dom.pagination.up.nav = nav
  self.dom.pagination.up.ul = ul

  if (self.search) {
    var form = getDom.Form()
    var divInput = getDom.Div('form-group row')
    var divInput2 = getDom.Div('col-xs-12 input-group')
    var input = getDom.Input('search', '搜索')
    var span = getDom.Span('input-group-btn')
    var button = getDom.Button('')
    var i = $('<i class="fa fa-search"></i>')

    $(button).append(i)
    $(span).append(button)
    $(divInput2).append(input).append(span)
    $(divInput).append(divInput2)
    $(form).append(divInput)
    $(divSearch).append(form)

    self.dom.search.form = form
    self.dom.search.input = input
    self.dom.search.submit = button

    $(form).submit(function() {
      self.update()
    })
    $(button).click(function() {
      self.update()
    })
  }

  return divBetween
}

SATable.getLimit = function() {
  var self = this
  var pageNumberData = SATable.getFormData(self.dom.pageNumber.form)
  var pageNumber = pageNumberData.pageNumber
  return pageNumber
}

SATable.createBarBottom = function() {
  var self = this
  var getDom = SATable.getDom

  var divBetween = getDom.RowBetween()
  var divPageNumber = getDom.Div('col-md-5')
  var divPage = $(self.dom.pagination.up.div).clone(true)
  $(divBetween).append(divPageNumber).append(divPage)

  self.dom.pagination.bottom = {}
  self.dom.pagination.bottom.div = divPage

  var formPageNumber = getDom.Form()
  var divSelect = getDom.InputSelect('pageNumber', '每页', [
    { text: '1', value: '1' },
    { text: '2', value: '2' },
    { text: '5', value: '5' },
    { text: '10', value: '10' },
    { text: '20', value: '20', selected: true },
    { text: '50', value: '50' },
    { text: '100', value: '100' },
    { text: '200', value: '200' }
  ])
  $(formPageNumber).append(divSelect)
  $(divPageNumber).append(formPageNumber)

  self.dom.pageNumber.div = divPageNumber
  self.dom.pageNumber.form = formPageNumber

  $(formPageNumber).change(function() {
    self.limit = self.getLimit()
    self.update()
  })

  return divBetween
}

SATable.createTable = function() {
  var self = this
  var getDom = SATable.getDom

  var div = getDom.Div()
  var table = getDom.Table()
  var tHead = getDom.THead()
  var tBody = getDom.TBody()
  var tr = getDom.Tr()

  $(tHead).append(tr)
  $(table).append(tHead).append(tBody)
  $(div).append(table)

  self.dom.table.head = tHead
  self.dom.table.headTr = tr
  self.dom.table.body = tBody

  return div
}

SATable.initTable = function() {
  var self = this
  var getDom = SATable.getDom

  var divContainer = getDom.Container()
  self.dom.divContainer = divContainer;

  var divError = getDom.Div('column justify-content-sm-center jumbotron bg-faded');
  self.dom.divError = divError;
  divError.hide();

  // head
  $(divContainer).append(self.createHead())
  if (self.hasFilter()) {
    $(divContainer).append(getDom.Br()).append(self.createFilterForm())
  } else {
    $(divContainer).append(getDom.Br())
  }
  // bar up
  $(divContainer).append(self.createBarUp())
  // table
  $(divContainer).append(self.createTable())
  // bar bottom
  %(divContainer).append(self.createBarBottom())

  // 每页显示结果数量
  self.limit = self.getLimit()

  $('#' + self.id).append(divContainer).append(divError)
}

SATable.initData = function(tableInfo) {
  var self = this

  self.id = tableInfo.id
  self.title = tableInfo.title
  self.columns = tableInfo.columns ? tableInfo.columns : []
  self.filters = tableInfo.filters ? tableInfo.filters : []
  self.search = tableInfo.search ? tableInfo.search : false
  self.requestGenerator = tableInfo.requestGenerator
  self.dataGenerator = tableInfo.dataGenerator
  self.page = tableInfo.page ? 1 : tableInfo.page
  self.createURL = tableInfo.createURL ? tableInfo.createURL : null
  self.extraData = tableInfo.extraData ? tableInfo.extraData : {}
  self.curPage = 1

  var cols = self.columns
  for (var i in cols) {
    var col = cols[i]
    if (col.sort && (col.ordering != -1 && col.ordering != 0 && col.ordering != 1)) {
      col.ordering = 0
    }
  }

  self.errorMessage = {  //错误信息采用覆盖策略。传入的自定义信息会覆盖默认的处理文本。
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
  if(tableInfo.errorMessage){
    for(var em in tableInfo.errorMessage)self.errorMessage[em] = tableInfo.errorMessage[em];
  }
  self.errorCustomField = tableInfo.errorCustomField ? tableInfo.errorCustomField : 'cause';
  self.errorCustom = tableInfo.errorCustom ? tableInfo.errorCustom : { }; //来自406的错误信息与其他错误信息分开管理。

  var tableIDs = {}
  tableIDs.id = self.id + 'SAT'
  tableIDs.filterBtn = tableIDs.id + 'FB'
  tableIDs.filterDiv = tableIDs.id + 'FD'
  tableIDs.filterForm = tableIDs.id + 'F'
  self.tableIDs = tableIDs

  var dom = {}
  dom.filter = {}
  dom.search = {}
  dom.pagination = {}
  dom.table = {}
  dom.pageNumber = {}
  self.dom = dom
}

SATable.getPaginationLi = function(page, curPage) {
  var getDom = this.getDom
  var li = getDom.Li('page-item')
  var a = getDom.A(page, 'javascript:void(0)', 'page-link')
  $(li).append(a)
  if (page == curPage) {
    $(li).addClass('active')
  }
  return li
}

SATable.getPaginationLiIgnore = function() {
  var getDom = SATable.getDom
  var li = getDom.Li('page-item disabled')
  var a = getDom.A('…', 'javascript:void(0)', 'page-link')
  $(li).append(a)
  return li
}

SATable.fillPagination = function(data) {
  var self = this
  var getDom = SATable.getDom

  var curPage = self.curPage
  var page_max = Math.ceil(data.count / self.limit)

  var liLast = getDom.Li('page-item page-prev')
  var liNext = getDom.Li('page-item page-next')
  var aLast = getDom.A(i, 'javascript:void(0)', 'page-link')
  var aNext = $(aLast).clone()
  $(aLast).append(getDom.IconLast())
  $(aNext).append(getDom.IconNext())
  $(liLast).append(aLast)
  $(liNext).append(aNext)

  var ul = self.dom.pagination.up.ul
  $(ul).append(liLast)
  if (page_max <= 7) {
    for (var i = 1; i <= page_max; ++i) {
      ul.append(SATable.getPaginationLi(i, curPage))
    }
  } else if (curPage <= 3) {
    for (var i = 1; i <= 4; ++i) {
      ul.append(SATable.getPaginationLi(i, curPage))
    }
    ul.append(SATable.getPaginationLiIgnore)
    ul.append(SATable.getPaginationLi(page_max, curPage))
  } else if (curPage >= page_max - 2) {
    ul.append(SATable.getPaginationLi(1, curPage))
    ul.append(SATable.getPaginationLiIgnore)
    for (var i = page_max - 3; i <= page_max; ++i) {
      ul.append(SATable.getPaginationLi(i, curPage))
    }
  } else {
    ul.append(SATable.getPaginationLi(1, curPage))
    ul.append(SATable.getPaginationLiIgnore)
    ul.append(SATable.getPaginationLi(curPage - 1, curPage))
    ul.append(SATable.getPaginationLi(curPage, curPage))
    ul.append(SATable.getPaginationLi(curPage + 1, curPage))
    ul.append(SATable.getPaginationLiIgnore)
    ul.append(SATable.getPaginationLi(page_max, curPage))
  }
  $(ul).append(liNext)

  if (curPage == 1) {
    $(liLast).addClass('disabled')
  }
  if (curPage == page_max) {
    $(liNext).addClass('disabled')
  }

  var buttonsDom = $(self.dom.pagination.up.ul).children(':not(.page-prev):not(.page-next):not(.disabled)').find('.page-link')
  $(buttonsDom).click(function() {
    var number = parseInt($(this).text())
    self.curPage = number
    if (curPage != number) {
      self.update()
    }
  })
  $(aLast).click(function() {
    if (curPage > 1) {
      self.curPage -= 1
      self.update()
    }
  })
  $(aNext).click(function() {
    if (curPage < page_max) {
      self.curPage += 1
      self.update()
    }
  })

  var navBottom = $(self.dom.pagination.up.nav).clone(true)
  $(self.dom.pagination.bottom.div).append(navBottom)
}

SATable.flushPagination = function() {
  var self = this
  $(self.dom.pagination.up.ul).empty()
  $(self.dom.pagination.bottom.div).empty()
}

SATable.flushTable = function() {
  $(this.dom.table.body).empty()
  $(this.dom.table.headTr).empty()
}

SATable.setLoading = function() {
  var self = this
  var getDom = SATable.getDom

  self.flushTable()
  var div = getDom.Div('row justify-content-sm-center jumbotron bg-faded')
  var divContent = getDom.Div('col-1')
  var icon = getDom.IconLoading()
  $(divContent).append(icon)
  $(div).append(divContent)
  $(self.dom.table.headTr).append(div)
}

SATable.fillTableHead = function() {
  var self = this
  var getDom = SATable.getDom
  var columns = self.columns
  var headTr = self.dom.table.headTr

  for(var i in columns) {
    var column = columns[i]
    // 名称
    var th = getDom.Th()
    $(th).text(column.caption)
    // 分析排序
    if (column.sort) {
      var icon = null
      if (column.ordering == 1) {               // 升序
        icon = getDom.IconUp()
      } else if (column.ordering == -1) {       // 降序
        icon = getDom.IconDown()
      } else {                                  // 无序
        icon = getDom.IconNoDirection()
      }
      var link = $('<a class="ordering" href="javascript:void(0)"></a>')
      $(link).append(icon)
      $(th).append(link)
    }
    $(headTr).append(th)
  }

  $(headTr).find('a.ordering').click(function() {
    var index = $(this).parent().index()
    var column = self.columns[index]
    column.ordering += 1
    if (column.ordering > 1) {
      column.ordering = -1
    }
    self.update()
  })
}

SATable.fillTableBody = function(data) {
  var self = this
  var getDom = SATable.getDom
  var types = SATable.types
  var body = self.dom.table.body

  for (var i in data) {
    var obj = data[i]
    var tr = getDom.Tr()
    var columns = self.columns
    for (var j in columns) {
      var column = columns[j]
      var content = obj[column.name]
      var ret = content
      if (types[column.type]) {
        ret = types[column.type](content, column, obj)
      }
      var td = getDom.Td()
      $(td).append(ret)
      $(tr).append(td)
    }
    $(body).append(tr)
  }
}

SATable.fillTable = function(data) {
  var self = this
  self.flushPagination()
  self.fillPagination(data)
  self.flushTable()
  self.fillTableHead()
  self.fillTableBody(data.data)
}

SATable.fillError = function (self, status, data) {
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
    var customField = data[self.errorCustomField];
    if(customField){  // 目标字段被找到
      var causeText = self.errorCustom[customField];  // 查询对应的语法。
      if(!causeText){ // 没找到，试图找到else标记作为缺省。
        causeText = self.errorCustom['else']; // 默认以此作为else标记。
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
    var message = self.errorMessage[status];
    if(!message)message = self.errorMessage['else'];
    content = standardFunction(message.head, message.text, message.showData ? data : null);
  }
  self.dom.divError.html(content);
};

SATable.getRequest = function() {
  var self = this
  var dom = self.dom
  var request = {}

  // 生成筛选信息
  if (self.hasFilter()) {
    var filterData = SATable.getFormData(dom.filter.form)
    var filters = {}
    for (var i in filterData) {
      var it = filterData[i]
      if (it) {
        filters[i] = it
      }
    }
    request.filters = filters
  }

  // 生成搜索信息
  if (self.hasSearch()) {
    var searchData = SATable.getFormData(dom.search.form)
    var search = searchData.search
    if (search) {
      request.search = search
    }
  }

  // 生成排序信息
  var ordering = []
  var columns = self.columns
  for (var i in columns) {
    var column = columns[i]
    if (column.sort && column.ordering != 0) {
      ordering.push((column.ordering == 1 ? '' : '-') + column.name)
    }
  }
  if (ordering.length > 0) {
    request.ordering = ordering
  }

  // 获得每页显示结果数量
  request.limit = self.limit

  // 获得欲显示的页数
  var curPage = self.curPage
  request.page = curPage ? curPage : 1

  return request
}

SATable.update = function() {
  var self = this
  var getDom = getDom
  var dom = self.dom

  // 显示载入界面
  self.setLoading()

  // 获得数据
  var request = self.requestGenerator(self.getRequest())
  $.ajax({
    type: request.type,
    url: request.url,
    dataType: request.dataType,
    data: request.data,
    success: function(ret) {
      var data = self.dataGenerator(ret)
      self.fillTable(data)
    }, error: function (ret) {
        self.dom.divContainer.hide();
        self.dom.divError.show();
        var data = ret.responseJSON;
        self.fillError(self, ret.status, data);
    }
  })
}

SATable.SimpleAjaxTable = function(tableInfo) {
  saTable = {
    hasFilter: SATable.hasFilter,
    hasSearch: SATable.hasSearch,
    createFilterForm: SATable.createFilterForm,
    createHead: SATable.createHead,
    createBarUp: SATable.createBarUp,
    createBarBottom: SATable.createBarBottom,
    createTable: SATable.createTable,
    getLimit: SATable.getLimit,
    fillTableHead: SATable.fillTableHead,
    fillTableBody: SATable.fillTableBody,
    fillTable: SATable.fillTable,
    fillError: SATable.fillError,
    flushTable: SATable.flushTable,
    fillPagination: SATable.fillPagination,
    flushPagination: SATable.flushPagination,
    getRequest: SATable.getRequest,
    initTable: SATable.initTable,
    initData: SATable.initData,
    setLoading: SATable.setLoading,
    update: SATable.update,
  }
  saTable.initData(tableInfo)
  saTable.initTable()
  saTable.update()

  return saTable
}
