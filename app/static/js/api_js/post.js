var insertTemplate = function(post) {
    var p = post;
    var id = p.id;
    var img = p.img;
    var username = p.username;
    var timestamp = p.timestamp;
    var content = p.content;
    var template = `
        <div class="post-${id}">
            <div class="media">
                <a class="pull-left" href="#">
                    <img class="media-object" src=${img} alt="">
                </a>
                <div class="media-body">
                    <h4 class="media-heading">${username}
                        <small>${timestamp}</small>
                    </h4>
                    ${content}
                    <div class="post-footer">
                        <a href="/post/${post.id}">
                            <button type="button" class="btn btn-xs btn-info">评论</button>
                        </a>
                        <button type="button" class="btn btn-xs btn-danger button-delete"
                                 data-pid="${id}">删除</button>
                    </div>
                </div>
            </div>
            <hr>
        </div>
    `;
    $('.div-home-post').after(template);
    $('.div-profile-post').after(template);
};


var editPostForm = function () {
    var keys = [
        'post',
    ];
    var editPostPrefix = 'id-textarea-';
    var form = formFromKeys(keys, editPostPrefix);
    return form;
};


var addNewPost = function () {
    var form = editPostForm();
    var success = function (r) {
        if (r.success) {
            log('成功添加微博！');
            insertTemplate(r.data)
            $('#id-textarea-post').val('')
        }
    };
    vip.postAdd(form, success);
};


var deletePost = function(id) {
    var form = {
        id: id,
    }
    var success = function (r) {
        if (r.success) {
            log('成功删除微博！');
            var pos = '.post-' + id;
            $(pos).remove();
        }
    };
    vip.postDelete(form, success);
};




