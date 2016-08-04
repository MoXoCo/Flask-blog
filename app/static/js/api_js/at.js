var insertAtTemplate = function(ats) {
    for(var i = 0; i < ats.length; i++) {
        var at = ats[i];
        var name = at.username
        var time = at.timestamp;
        var id = at.post_id;
        var content = at.post;
        var t = `
            <a href="/post/${id}">
                <div>
                    <strong>${name}</strong>
                    <span class="pull-right text-muted">
                        <em>${time}</em>
                    </span>
                </div>
                <div>${content}</div>
            </a>
            <hr>
        `;
        $('#id-div-at').append(t);
    };
};


var changeButton = function(name) {
    var t = `
        <button type="button" class="btn btn-xs btn-success"
                data-name="${name}" id="id-button-up">
            0 个 <i class="fa fa-caret-up"></i>
        </button>
    `;
    $('#id-button-down').remove();
    $('#id-div-buttonchange').append(t);
};


var insertAtPost = function(name) {
    var form = {
        name: name,
    };
    var success = function (r) {
       if (r.success) {
           log('获得@');
           insertAtTemplate(r.data);
           changeButton(name);
       }
    };
    vip.atPostInsert(form, success);
};

var deleteAtPost = function(name) {
    $('#id-div-at').children().remove();
    var t = `
        <button type="button" class="btn btn-xs btn-success"
                data-name="${name}" id="id-button-down">
            0 个 <i class="fa fa-caret-down"></i>
        </button>
    `;
    $('#id-div-buttonchange').append(t)
    $('#id-button-up').remove();
};



