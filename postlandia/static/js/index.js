// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        add_mode: false,
        mouse: false,
        index: -1,
        new_comment: "",
        posts: [],
        current_user: "",
        likers: "",
        dislikers: "",
    }

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.complete = (post) => {
        // Initializes useful fields of post.
        post.map((p) => {
            p.rating = 0;
        })
    };

    app.reset_form = function(){
        app.vue.new_comment = "";
    }

    app.add_post = function(){
        axios.post(add_post_url,
            {
                text: app.vue.new_comment
            }).then(function (response) {
                app.vue.posts.push({
                    id: response.data.id,
                    text: app.vue.new_comment,
                    first_name: response.data.first_name,
                    last_name: response.data.last_name,
                    email: response.data.email,
                });
                axios.get(load_posts_url).then(function (response) {
                    app.vue.posts = app.enumerate(response.data.posts);
                });
                //app.enumerate(app.vue.posts);
                app.reset_form();
                app.set_add_status(false);
            });
    };

    app.set_add_status = function(new_status){
        app.vue.add_mode = new_status;
    };

    app.delete_post = function(post_idx){
        let id = app.vue.posts[post_idx].id;
        axios.get(delete_post_url, {params: {id: id}}).then(function (response){
            for (let i = 0; i < app.vue.posts.length; i++){
                if(app.vue.posts[i].id == id){
                    app.vue.posts.splice(i,1);
                    axios.get(load_posts_url).then(function (response) {
                        app.vue.posts = app.enumerate(response.data.posts);
                    });
                    app.enumerate(app.vue.posts);
                    break;
                }
            }
        });
    };

    app.like = function(post_idx){
        let post = app.vue.posts[post_idx];
        console.log(post)
        if(post.rating == 1){
            post.rating = 0;
        }else{
            post.rating = 1;
        }
        axios.post(set_rating_url, {post_id: post.id, rating: post.rating});
    };

    app.dislike = function(post_idx){
        let post = app.vue.posts[post_idx];
        if(post.rating == -1){
            post.rating = 0;
        }else{
            post.rating = -1;
        }
        axios.post(set_rating_url, {post_id: post.id, rating: -1});
    };

    app.like_list = function(post_idx){
        app.vue.mouse = true;
        let post = app.vue.posts[post_idx];
        app.vue.index = post_idx;
        axios.post(get_likers_url, {post_id: post.id}).then(function(response){
            app.vue.likers = response.data.s;
        });
    };

    app.mouseout_like = function(post_idx){
        app.vue.mouse = false;
        app.vue.likers = "";
        app.vue.index = -1;
    }

    app.dislike_list = function(post_idx){
        app.vue.mouse = true;
        let post = app.vue.posts[post_idx];
        app.vue.index = post_idx;
        axios.post(get_dislikers_url, {post_id: post.id}).then(function(response){
            app.vue.dislikers = response.data.s;
        });
    };

    app.mouseout_dislike = function(post_idx){
        app.vue.mouse = false;
        app.vue.likers = "";
        app.vue.index = -1;
    }

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        set_add_status: app.set_add_status,
        add_post: app.add_post,
        delete_post: app.delete_post,
        like: app.like,
        dislike: app.dislike,
        like_list: app.like_list,
        dislike_list: app.dislike_list,
        mouseout_like: app.mouseout_like,
        mouseout_dislike: app.mouseout_dislike,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        // Put here any initialization code.
        // Typically this is a server GET call to load the data.
        
        axios.get(load_posts_url).
            then(function (response) { //enumerate
                app.vue.posts = app.enumerate(response.data.posts);
                app.complete(app.vue.posts);
        })
        .then(() => {
            for(let p of app.vue.posts){
                axios.get(get_rating_url, {params: {post_id: p.id}})
                    .then((result) => {
                        p.rating = result.data.rating;
                    });
            }
        });
        
        axios.get(load_user_url).then(function(response) {
            app.vue.current_user = response.data.email;
        });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);