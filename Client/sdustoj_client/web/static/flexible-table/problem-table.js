/**
 * Created by guess on 2017/8/24.
 */
/* 用于生成题目添加页面的列表和zTree */

var ProblemTable = {}







var results = [
    {
        directory: ["root", 'first001','second001'],
        problem: {
            id: 11,
            name: "求和",
        }
    },
    {
        directory: ["root"],
        problem: {
            id: 12,
            name: "求差",
        }
    },
    {
        directory: ["root", 'first001','second02'],
        problem: {
            id: 13,
            name: "求几",
        }
    },
    {
        directory: ["root", 'first002','second001'],
        problem: {
            id: 14,
            name: "求啥",
        }
    },
    {
        directory: ["root", 'first003','second002'],
        problem: {
            id: 15,
            name: "求及诶诶额",
        }
    }
]

ProblemTable.getDom = {}

ProblemTable.getDom.Div = function(class_){
    var div = $("<div></div>")
    if(class_){
        div.addClass(class_)
    }
    return div
}

ProblemTable.getDom.IconEdit = function(class_) {
  var icon = $('<i class="fa fa-pencil-square-o fa-fw"></i>')
  if (class_) {
    $(icon).addClass(class_)
  }
  return icon
}

ProblemTable.getDom.IconSave = function(class_) {
  var icon = $('<i class="fa fa fa-floppy-o fa-fw"></i>')
  if (class_) {
    $(icon).addClass(class_)
  }
  return icon
}

ProblemTable.getDom.IconDelete = function(class_) {
  var icon = $('<i class="fa fa-trash fa-fw"></i>')
  if (class_) {
    $(icon).addClass(class_)
  }
  return icon
}

ProblemTable.getDom.Table = function (class_) {
    var table = $("<table></table>")
    if(class_){
        table.addClass(class_)
    }
    return table
}

ProblemTable.getDom.Thead = function (class_) {
    var thead = $("<thead></thead>")
    if(class_){
        thead.addClass(class_)
    }
    return thead
}

ProblemTable.getDom.Tr = function (class_){
    var tr = $("<tr></tr>")
    if(class_){
        tr.addClass(class_)
    }
    return tr
}

ProblemTable.getDom.Th = function (class_) {
    var th = $("<th></th>")
    if(class_){
        th.addClass(class_)
    }
    return th
}

ProblemTable.getDom.Td = function (class_){
    var td = $("<td></td>")
    if(class_){
        td.addClass(class_)
    }
    return td
}

ProblemTable.getDom.P = function (class_){
    var p = $('<p></p>')
    if(class_){
        p.addClass(class_)
    }
    return p
}

ProblemTable.getDom.Input = function (class_, type){
    var input = $("<input>")
    if(class_){
        input.addClass(class_)
    }
    if(type){
        input.attr("type", type)
    }
    return input
}

ProblemTable.getDom.Select = function(class_){
    var select = $("<select></select>")
    if(class_){
        select.addClass(class_)
    }
    return select
}

ProblemTable.getDom.Option = function(class_){
    var option = $("<select></select>")
    if(class_){
        option.addClass(class_)
    }
    return option
}

ProblemTable.getDom.Button = function (class_, value) {
    var button = $("<button></button>")
    if(class_){
        button.addClass(class_)
    }
    if(value){
        button.text(value)
    }
    return button
}

//初始化表格信息：条目，请求数据地址，标题
ProblemTable.initTable = function (tableInfo) {
    var self = this
    self.tableInfo = tableInfo
    self.id = tableInfo.id
    self.url = tableInfo.url
    self.update_url = tableInfo.update_url
    self.success_url = tableInfo.success_url
    self.column = tableInfo.column
    self.dom = {}
    var getDom = ProblemTable.getDom
    var table = getDom.Table("table")
    var thead = getDom.Thead()
    var th = getDom.Th()
    var column = self.column
    for(var i in column){
        var th = getDom.Th()
        th.text(column[i].title)
        thead.append(th)
    }
    table.append(thead)
    self.dom.table = table
}

var text = function(key, val, readOnly){
    var getDom = ProblemTable.getDom
    var p = getDom.P()
    var div = getDom.Div()
    p.text(val)
    div.append(p)
    if(!readOnly){
        var input = getDom.Input("form-control", "text")
        input.val(val)
        input.hide()
        div.append(input)
    }
    return {
        div: div,
        toRead: function(){
            p.show()
            if(!readOnly){
                input.hide()
                p.text(input.val())
            }
        },
        toWrite: function(){
            if(!readOnly){
                p.hide()
                input.show()
            }
        },
        getValue: function(){
            if(readOnly){
                return val
            }else{
                return input.val()
            }
        },
        setValue: function(v){
            p.text(v)
            if(!readOnly){
                input.text(v)
            }
        },
        isReadOnly: function(){
            return readOnly
        },
        getKey: function(){
            return key
        },
    }
}

var select = function(key, val, readOnly){
    var getDom = ProblemTable.getDom
    var p = getDom.P()
    var div = getDom.Div()
    p.text(val? "是":"否")
    div.append(p)
    if(!readOnly){
        var input = getDom.Select("form-control")
        var optionTrue = $('<option></option>')
        var optionFalse = $('<option></option>')
        $(optionTrue).val(true).text('是')
        $(optionFalse).val(false).text('否')
        $(input).append(optionTrue).append(optionFalse).hide()
        if (val == true) {
          $(optionTrue).attr('selected', 'selected')
        } else if (val == false) {
          $(optionFalse).attr('selected', 'selected')
        }
    }
    div.append(input)
    return {
        div: div,
        toRead: function(){
            if(!readOnly){
                input.hide()
                var val = input.val()
                if(val == 'true'){
                    p.text("是")
                }else{
                    p.text("否")
                }
            }
            p.show()
        },
        toWrite: function(){
            if(!readOnly){
                p.hide()
                input.show()
            }
        },
        getValue: function(){
            if(readOnly){
                return val
            }else{
                return input.val()
            }
        },
        setValue: function(v){
            p.text(v)
            if(!readOnly){
                input.text(v)
            }
        },
        isReadOnly: function(){
            return readOnly
        },
        getKey: function(){
            return key
        },
    }
}

var tool = {
    text: text,
    select: select,
}

var updateDatabase = function(database, row, newdata){
    if(newdata){
        for(var i in newdata){
            row[i] = newdata[i]
        }
    }else{
        var index = $.inArray(row, database)
        database.splice(index, 1)
    }
}

ProblemTable.updateRow = function(row){
    var self = this
    is_exit = false
    for(var i in self.database){
        if(self.database[i].problem_id == row.problem_id){
            is_exit = true
            break
        }
    }
    if(is_exit){
        alert("该题目已被添加")
    }else
    {
        self.database[self.database.length] = row
        var getDom = ProblemTable.getDom
        var tr = getDom.Tr()
        var column = self.column
        var itemlist = []
        for(var i in column){
            var td = getDom.Td()
            var type = column[i].type
            var key = column[i].name
            var val = row[key]
            var readOnly = column[i].readOnly
            var item = tool[type](key, val, readOnly)
            itemlist[itemlist.length] = item
            td.append(item.div)
            tr.append(td)
        }
        //编辑
        var td = getDom.Td()
        var iconEdit = getDom.IconEdit()
        //保存
        var td = getDom.Td()
        var iconSave = getDom.IconSave()
        iconSave.hide()
        iconEdit.click(function(){
            iconSave.show()
            iconEdit.hide()
            for(var i in itemlist){
                itemlist[i].toWrite()
            }
        })
        iconSave.click(function(){
            iconEdit.show()
            iconSave.hide()
            var newdata = {}
            for(var i in itemlist){
                itemlist[i].toRead()
                if(!itemlist[i].isReadOnly()){
                    newdata[itemlist[i].getKey()] = itemlist[i].getValue()
                }
            }
            updateDatabase(self.database, row, newdata)
        })
        td.append(iconEdit).append(iconSave)
        tr.append(td)
        //删除
        var td = getDom.Td()
        var iconDelete = getDom.IconDelete()
        iconDelete.click(function(){
            tr.remove()
            updateDatabase(self.database, row, "")
        })
        td.append(iconDelete)
        tr.append(td)
        var table = self.dom.table
        table.append(tr)
        $("#"+ self.id).append(table)
    }
}

ProblemTable.update = function (data){
    var self = this
    for(var i in data){
        self.updateRow(data[i])
    }
    $("#update").click(function () {
        var url = self.update_url
        $.ajax({
            type: "POST",
            url: url,
            data: {dataStr: JSON.stringify(self.database)},
            datatype: "JSON",
            success: function () {
                alert("成功")
                location.href = self.success_url
            },
            error: function () {
                alert("error")
            }
        })
    })
}

//请求数据
ProblemTable.initData = function () {
    var self = this
    var data = self.tableInfo.data
    var url = self.url
    var data = {}
    data.limit = 10000
    $.ajax({
        type: "GET",
        url: url,
        data: data,
        datatype: "JSON",
        success: function (ret) {
            var data = ret.results
            self.update(data)
        }
    })
}

ProblemTable.updateDir = function(zTreeObj, ret){
    treedata = this.treedata
    var results = ret.results
    for(var i in results){
        var info = results[i]
        var dirs = info.directory
        dirs.unshift(info.category)
        var pro = info.problem
        var curNode = null
        for(var i in dirs){
            var dir = dirs[i]
            var node = zTreeObj.getNodeByParam('name', dir, curNode)
            if (node == null) {
              node = zTreeObj.addNodes(parentNode=curNode, newNodes=[{name: dir}], isSilent=true)[0]
            }
            curNode = node
        }
        treedata[pro.id] = pro.title
          strAdd = "(" + pro.id + ")" + pro.title
          // if (!info.available) {
          //   strAdd = "<label class=\"text-danger\">" + strAdd + "</label>"
          // } else {
          //   strAdd = "<label>" + strAdd + "</label>"
          // }
          zTreeObj.addNodes(parentNode=curNode, newNodes={ name: strAdd, id: pro.id}, isSilent=true)
    }
}

ProblemTable.initTree = function(treeInfo){
    var self = this
    self.treeInfo = treeInfo
    var zTreeObj = null
    var setting = {
        callback:{
            onClick: function(event, treeId, treeNode){
                if(treeNode.isParent) {} else{
                    var row = {}
                    row.problem_id= treeNode.id
                    row.title = treedata[treeNode.id]
                    row.weight = 1
                    row.available = true
                    row.deleted = false
                    self.updateRow(row)
                }
            }
        },
    }
    var zNodes = []
    zTreeObj = $.fn.zTree.init($("#tree"), setting, zNodes);
    var url = treeInfo.url
    var data = { limit: 10000}
    $.ajax({
        type: "GET",
        url: url,
        data: data,
        datatype: "JSON",
        success: function (ret) {
            self.updateDir(zTreeObj, ret)
        }
    })
}

ProblemTable.Table = function(tableInfo, treeInfo){
    var problemTable = {
        database: [],
        treedata: {},
        initTable: ProblemTable.initTable,
        initData: ProblemTable.initData,
        initTree: ProblemTable.initTree,
        createTable: ProblemTable.createTable,
        update: ProblemTable.update,
        updateRow: ProblemTable.updateRow,
        addRow: ProblemTable.addRow,
        updateDir: ProblemTable.updateDir,
    }
    problemTable.initTable(tableInfo)
    problemTable.initData()
    if(treeInfo){
        problemTable.initTree(treeInfo)
    }
}