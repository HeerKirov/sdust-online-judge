function test_output(something) {
  alert(JSON.stringify(something))
}

function getFormData(form) {
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