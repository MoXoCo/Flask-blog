var insertTemplate = function(comment) {
    var p = comment;
    var id = p.id;
    var img = p.img;
    var username = p.username;
    var timestamp = p.timestamp;
    var content = p.content;
    var template = `
        <div class="div-comments">
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
                        <button type="button" class="btn btn-xs btn-danger"
                                id="id-button-delete" data-cid="${id}">删除</button>
                    </div>
                </div>
            </div>
            <hr>
        </div>
    `;
    $('.comment').append(template);
};


var editCommentForm = function () {
    var keys = [
        'comment',
    ];
    var editPostPrefix = 'id-input-';
    var form = formFromKeys(keys, editPostPrefix);
    return form;
};

var addNewComment = function () {
    var form = editCommentForm ();
    var success = function (r) {
        if (r.success) {
            log('comment add success： ',typeof r, r);
            log('成功添加评论！');
            insertTemplate(r.data)
            $('#id-input-comment').val('')
        }
    };
    vip.commentAdd(form, success);
};

var deleteComment = function(id, self) {
    var form = {
        id: id,
    }
    var success = function (r) {
        if (r.success) {
            log('成功删除微博！');
            self.closest('.div-comments').remove();
        }
    };
    vip.commentDelete(form, success);
};




