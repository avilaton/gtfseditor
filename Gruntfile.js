module.exports = function(grunt) {
  'use strict';

  // Load grunt tasks automatically
  require('load-grunt-tasks')(grunt);

  // Time how long tasks take. Can help when optimizing build times
  require('time-grunt')(grunt);

console.log(require('./bower.json').directory);

  grunt.initConfig({

    // Project settings
    yeoman: {
      // configurable paths
      app: require('./bower.json').appPath || './',
      dist: 'dist'
    },
		handlebars: {
		  compile: {
		    options: {
		      namespace: "JST",
		      amd: true,
					processName: function (filePath) {
						var file = filePath.replace('templates/','');
						var templatePath = file.split('.')[0];
						return templatePath;
					},
					// partialRegex: /.*/,
					// partialsPathRegex: /src\/common\/templates\/partials\//,
					// processPartialName: function(filePath) {
					// 	var file = filePath.replace('src/common/templates/partials/','');
					// 	var templatePath = file.split('.')[0];
					// 	return templatePath;
				 //  }
		    },
		    files: {
		      // "path/to/result.js": "path/to/source.hbs",
		      "scripts/JST.js": ["templates/**/*.handlebars"]
		    }
		  }
		},

				options: {

				},

    // The actual grunt server settings
    connect: {
      options: {
        port: 9000,
        keepalive: true,
        // Change this to '0.0.0.0' to access the server from outside.
        hostname: '0.0.0.0',
        livereload: 35729
      },
      livereload: {
        options: {
          open: true,
          base: [
            '.tmp',
            '<%= yeoman.app %>'
          ]
        }
      }
    },
    // Watches files for changes and runs tasks based on the changed files
    watch: {
      js: {
        files: ['scripts/{,**/}*.js'],
        // files: ['{.tmp,<%= yeoman.app %>}/scripts/{,**/}*.js'],
        tasks: ['handlebars']
      },
      hbs: {
        files: ['templates/{,**/}*.handlebars'],
        tasks: ['handlebars']
      },
//      jsTest: {
//        files: ['test/spec/{,*/}*.js'],
//        tasks: ['newer:jshint:test', 'karma']
//      },
      // compass: {
      //   files: ['<%= yeoman.app %>/styles/{,**/}*.{scss,sass}'],
      //   tasks: ['compass:server'] //, 'autoprefixer'
      // },
      // styles: {
      //   files: ['<%= yeoman.app %>/styles/{,**/}*.css'],
      //   tasks: ['newer:copy:styles', 'autoprefixer']
      // },
      // gruntfile: {
      //   files: ['Gruntfile.js']
      // },
      livereload: {
        options: {
          livereload: '<%= connect.options.livereload %>'
        },
        files: [
          'scripts/{,**/}*.js'
          // '<%= yeoman.app %>/{,**/}*.html',
          // '.tmp/styles/{,**/}*.css',
          // '<%= yeoman.app %>/images/{,**/}*.{png,jpg,jpeg,gif,webp,svg}'
        ]
      }
    },
  });

  // By default, lint and run all tests.
  grunt.registerTask('monitor', [
    'watch:livereload'
  ]);

  grunt.registerTask('serve', [
    'connect:livereload',
    'watch'
  ]);

  grunt.registerTask('default', [
  ]);

};