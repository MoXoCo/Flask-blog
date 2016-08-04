var insertFollowTemplate = function(name) {
    var t = `
        <button type="button" class="btn btn-danger"
            id="id-button-unfollow" data-name="${name}">取关</button>
    `;
    $('#id-button-follow').remove();
    $('#div-button').append(t);
};

var insertUnfollowTemplate = function(name) {
    var t = `
        <button type="button" class="btn btn-primary"
            id="id-button-follow" data-name="${name}">关注</button>
    `;
    $('#id-button-unfollow').remove();
    $('#div-button').append(t);
};

var followUser = function(name) {
    var form = {
        name: name
    };
    var success = function (r) {
       if (r.success) {
           log('关注！');
           insertFollowTemplate(name);
       }
    };
    vip.userFollow(form, success);
};

var unfollowUser = function(name) {
    var form = {
        name: name
    };
    var success = function (r) {
       if (r.success) {
           log('取关！');
           insertUnfollowTemplate(name);
       }
    };
    vip.userUnFollow(form, success);
};



