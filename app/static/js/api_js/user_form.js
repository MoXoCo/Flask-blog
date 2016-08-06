var insertFormTemplate = function(msg) {
    var name = msg.username;
    var address = msg.address;
    var profession = msg.profession;
    var company = msg.company;
    var position = msg.position;
    var education = msg.education;
    var signature = msg.signature;
    var t = `
        <div class="col-lg-4" id="id-div-insertform">
            <div class="panel panel-default">
                <div class="panel-body">
                    <div role="form">
                        <div class="form-group">
                            <label>居住地</label>
                            <input class="form-control" id="id-input-address" value="${address}">
                        </div>
                        <div class="form-group">
                            <label>行业</label>
                            <input class="form-control" id="id-input-profession" value="${profession}">
                        </div>
                        <div class="form-group">
                            <label>公司 </label>
                            <input class="form-control" id="id-input-company" value="${company}">
                        </div>
                        <div class="form-group">
                            <label>职位</label>
                            <input class="form-control" id="id-input-position" value="${position}">
                        </div>
                        <div class="form-group">
                            <label>教育</label>
                            <input class="form-control" id="id-input-education" value="${education}">
                        </div>
                        <div class="form-group">
                            <label>个性签名</label>
                            <input class="form-control" id="id-input-signature" value="${signature}">
                        </div>
                        <button type="button" class="btn btn-outline btn-primary pull-right"
                            id="id-button-submit-form"
                            data-name="${name}">提交</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    var btn = `
        <button type="button" class="btn btn-outline btn-default pull-right"
            id="id-button-form-left"
            data-name="${name}"><i class="glyphicon glyphicon-chevron-left"></i>填写资料</button>
    `;
    $('#id-div-form').after(t);
    $('#id-button-form-right').remove();
    $('#id-div-button-form').append(btn);
};

var deleteFormTemplate = function(name) {
    var btn = `
        <button type="button" class="btn btn-outline btn-default pull-right"
            id="id-button-form-right"
            data-name="${name}">填写资料<i class="glyphicon glyphicon-chevron-right"></i></button>
    `;
    $('#id-div-insertform').remove();
    $('#id-button-form-left').remove();
    $('#id-div-button-form').append(btn);
};

var insertMsgForm = function(name) {
    var form = {
        name: name,
    };
    var success = function(r) {
        if (r.success) {
            insertFormTemplate(r.data);
        }
    };
    vip.formMsg(form, success);
}

var submitForm = function(name) {
    var keys = [
        'address',
        'profession',
        'company',
        'position',
        'education',
        'signature',
    ];
    var prefix = 'id-input-';
    var form = formFromKeys(keys, prefix);
    form.name = name;
    var success = function(r) {
        if(r.success) {
            log('form submit success');
            window.location.href = r.next;
        }
    };
    vip.formSubmit(form, success);
};




