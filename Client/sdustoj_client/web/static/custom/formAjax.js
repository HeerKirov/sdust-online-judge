// 修改自Django Rest Framework

function doAjaxSubmit(e) {
  var form = $(this);
  var btn = $(this.clk);
  var method = (
    btn.data('method') ||
    form.data('method') ||
    form.attr('method') || 'GET'
  ).toUpperCase();

  if (method === 'GET') {
    // GET requests can always use standard form submits.
    return;
  }

  var contentType =
    form.find('input[data-override="content-type"]').val() ||
    form.find('select[data-override="content-type"] option:selected').text();

  if (method === 'POST' && !contentType) {
    // POST requests can use standard form submits, unless we have
    // overridden the content type.
    return;
  }

  // At this point we need to make an AJAX form submission.
  e.preventDefault();

  var url = form.attr('action');
  var data;

  if (contentType) {
    data = form.find('[data-override="content"]').val() || ''
  } else {
    contentType = form.attr('enctype') || form.attr('encoding')

    if (contentType === 'multipart/form-data') {
      if (!window.FormData) {
        alert('Your browser does not support AJAX multipart form submissions');
        return;
      }

      // Use the FormData API and allow the content type to be set automatically,
      // so it includes the boundary string.
      // See https://developer.mozilla.org/en-US/docs/Web/API/FormData/Using_FormData_Objects
      contentType = false;
      data = new FormData(form[0]);
    } else {
      contentType = 'application/x-www-form-urlencoded; charset=UTF-8'
      data = form.serialize();
    }
  }

  var ret = $.ajax({
    url: url,
    method: method,
    data: data,
    contentType: contentType,
    processData: false,
    success: function(ret) {
      if (method == 'PATCH' || method == 'PUT') {
        //location.reload()
        alert("成功")
      } else {
        //location.reload()
        alert("成功")
      }
    },
    error: function(a, b, c) {
      test_output(a.responseJSON)
    }
  });

  return ret;
}

function captureSubmittingElement(e) {
  var target = e.target;
  var form = this;

  form.clk = target;
}

$.fn.ajaxForm = function() {
  var options = {}

  return this
    .unbind('submit.form-plugin  click.form-plugin')
    .bind('submit.form-plugin', options, doAjaxSubmit)
    .bind('click.form-plugin', options, captureSubmittingElement);
};

$(document).ready(function() {
  $('form').ajaxForm();
});
