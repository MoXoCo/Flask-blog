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
    log('div: ', div)
    $('#div-button').append(t);
};

// follower
var insertFollowFollowerTemplate = function(name, id) {
    var t = `
        <button type="button" class="btn btn-xs btn-danger"
            id="id-button-unfollow-follower" data-name="${name}"
            data-id="${id}">取关</button>
    `;
    var div = '#id-div-follow-' + id;
    $(div).children().remove('#id-button-follow-follower');
    $(div).append(t);
};

var insertUnfollowFollowerTemplate = function(name, id) {
    var t = `
        <button type="button" class="btn btn-xs btn-primary"
            id="id-button-follow-follower" data-name="${name}"
            data-id="${id}">关注</button>
    `;
    var div = '#id-div-follow-' + id;
    $(div).children().remove();
    $(div).append(t);
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

// follower
var followFollower = function(name, id) {
    var form = {
        name: name
    };
    var success = function (r) {
       if (r.success) {
           log('关注！');
           insertFollowFollowerTemplate(name, id);
       }
    };
    vip.userFollow(form, success);
};

var unfollowFollower = function(name, id) {
    var form = {
        name: name
    };
    var success = function (r) {
       if (r.success) {
           log('取关！');
           insertUnfollowFollowerTemplate(name, id);
       }
    };
    vip.userUnFollow(form, success);
};



