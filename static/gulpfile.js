// Include gulp
var path = require('path');
var gulp = require('gulp');
var gutil = require('gulp-util');
var bg = require("gulp-bg");
// Include Our Plugins
var jshint = require('gulp-jshint');
//var sass = require('gulp-ruby-sass');
// var sass = require('gulp-sass');
var coffee = require('gulp-coffee');
var rjs = require('gulp-requirejs');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');
var browserify = require('gulp-browserify');

// Lint Task
gulp.task('lint', function () {
    return gulp.src('js/*.js')
        .pipe(jshint().on('error', gutil.log))
        .pipe(jshint.reporter('default'));
});

// Compile Our Sass
// gulp.task('sass', function () {
//    return gulp.src('scss/[^_]*.scss')
//        .pipe(sourcemaps.init())
//        .pipe(sass({outputStyle: 'compressed'}))
//        .on('error', gutil.log)
//        .pipe(sourcemaps.write('.'))
//        .pipe(gulp.dest('build/css'));
// });
// node-sass have a bug will crash when with sourcemap enabled,
// So just run a node-sass command
gulp.task("sass",
  bg("node-sass",
    "--source-map",
    '--output-style', 'compressed',
    'scss/main.scss',
    'build/css/main.css'
  )
);

//coffee

gulp.task('coffee', function () {
    gulp.src('coffee/*.coffee')
        .pipe(sourcemaps.init())
        .pipe(coffee({bare: true}).on('error', gutil.log))
        .pipe(sourcemaps.write('./'))
        .pipe(gulp.dest('build/js'));
});


// Watch Files For Changes
gulp.task('watch', function () {
    gulp.watch('js/*.js', ['lint']);
    //gulp.watch('js/*.js', ['lint', 'rjs']);
    //gulp.watch('game/*.js', ['browserify']);
    //gulp.watch('game/*/*.js', ['browserify']);
    gulp.watch('scss/**/*.scss', ['sass']);
    gulp.watch('coffee/*.coffee', ['coffee']);
});


//r.js
//gulp.task('rjs', function () {
    //rjs({
        //baseUrl: "./js/",
        //out: "app.js",
        //mainConfigFile: "./js/main.js",
        //name: 'main',
        //removeCombined: true
    //}).on('error', gutil.log).pipe(uglify())
        //.pipe(gulp.dest('./deploy/'));
//});


//build Game
//gulp.task('browserify', function () {
    //return gulp.src('game/main.js')
        //.pipe(browserify())
        //.pipe(uglify())
        //.pipe(gulp.dest('./deploy/'));
        //});
parent = path.resolve(process.cwd(), '..');
manage = path.join(parent, "manage.py");

gulp.task("server",bg("python", manage, "runserver", "0.0.0.0:8000"));

// Default Task
gulp.task('default', ['sass', 'coffee', 'watch', 'server']);





