SATable.DRF = {}

SATable.DRF.dataGenerator = function(data) {
  return {
    count: data.count,
    data: data.results
  }
}

SATable.DRF.requestGenerator = function(request) {
  var data = {}

  // 筛选项
  if (this.hasFilter()) {
    var filters = request.filters
    for (var i in request.filters) {
      data[i] = filters[i]
    }
  }
  // 搜索
  if (this.hasSearch()) {
    data.search = request.search
  }
  // 排序
  if (request.ordering) {
    var ordering = request.ordering
    var o = ''
    var first = true
    for (var i in ordering) {
      if (first) {
        first = false
      } else {
        o += ','
      }
      o += ordering[i]
    }
    data.ordering = o
  }
  // 每页显示数量
  data.limit = request.limit
  // 显示第几页
  offset = (request.page - 1) * request.limit
  data.offset = offset

  var ret = {
    type: 'get',
    url: this.extraData.url,
    dataType: 'json',
    data: data
  }

  return ret
}

SATable.DRFTable = function(tableInfo) {
  tableInfo.extraData = { url: tableInfo.url }
  tableInfo.requestGenerator = SATable.DRF.requestGenerator
  tableInfo.dataGenerator = SATable.DRF.dataGenerator
  saTable = SATable.SimpleAjaxTable(tableInfo)
}

SATable.DRF.keepRequest = function(saForm, selectDom, item, ret) {
  if (ret.next != null) {
    item.ajaxInfo.url = ret.next
    saForm.requestSelectData(saForm, selectDom, item)
  }
}

SATable.DRF.keepRequestValue = function(saForm, selectDom, item, ret, value) {
  if (ret.next != null) {
    item.ajaxInfo.url = ret.next
    saForm.requestSelectData(saForm, selectDom, item, value)
  }
}
