module.exports = function(grunt) {
  'use strict';

  // Load grunt tasks automatically
  require('load-grunt-tasks')(grunt);

  // Time how long tasks take. Can help when optimizing build times
  require('time-grunt')(grunt);

  grunt.initConfig({

    // Project settings
    yeoman: {
      // configurable paths
      app: require('./bower.json').directory || './',
      dist: 'dist'
    },
    requirejs: {
      prod: {
        options: {
          almond: true,
          wrap: true,
          baseUrl: "app/scripts",
          name: "../bower_components/almond/almond",
          // exclude: ["OpenLayers"],
          include: ["main"],
          mainConfigFile: "app/scripts/main.js",
          out: "dist/scripts/main.js",
          optimize: 'uglify'
        }
      }
    },
		handlebars: {
		  compile: {
		    options: {
		      namespace: "JST",
		      amd: true,
					processName: function (filePath) {
						var file = filePath.replace('./app/templates/','');
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
		      "./app/scripts/JST.js": ['<%= yeoman.app %>' + '/templates/**/*.handlebars']
		    }
		  }
		},
    copy: {
      main: {
        files: [
          {expand: true, cwd: 'app/', src: ['vendor/**'], dest: 'dist/scripts/'},

          {expand: true, cwd: 'app/', src: ['styles/**'], dest: 'dist/'},

          {expand: true, cwd: 'app/bower_components/bootstrap/dist/', src: ['css/**', 'fonts/**'], dest: 'dist/styles/bootstrap'},

          {src: ['app/index.prod.html'], dest: 'dist/index.html'}
        ],
      },
    },

    // The actual grunt server settings
    connect: {
      options: {
        port: 9000,
        // keepalive: true,
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
      },
      dist: {
        options: {
          open: true,
          base: [
            '<%= yeoman.dist %>'
          ]
        }
      }
    },
    jshint: {
        options: {
            jshintrc: '.jshintrc'
        },
        all: [
            'Gruntfile.js',
            'app/scripts/{,**/}*.js',
            '!app/scripts/JST.js'
        ]
    },
    // Watches files for changes and runs tasks based on the changed files
    watch: {
      js: {
        files: ['app/scripts/{,**/}*.js'],
        // files: ['{.tmp,<%= yeoman.app %>}/scripts/{,**/}*.js'],
        tasks: ['jshint']
      },
      hbs: {
        files: ['app/templates/{,**/}*.handlebars'],
        tasks: ['handlebars']
      },
      livereload: {
        options: {
          livereload: '<%= connect.options.livereload %>'
        },
        files: [
          'app/scripts/{,**/}*.js',
          'app/templates/{,**/}*.handlebars'
          // '<%= yeoman.app %>/{,**/}*.html',
          // '.tmp/styles/{,**/}*.css',
          // '<%= yeoman.app %>/images/{,**/}*.{png,jpg,jpeg,gif,webp,svg}'
        ]
      }
    },
  });

  // By default, lint and run all tests.
  grunt.registerTask('build', [
    'handlebars',
    'copy',
    'requirejs:prod'
  ]);

  grunt.registerTask('serve', [
    'connect:livereload',
    'watch'
  ]);

  grunt.registerTask('serve:dist', [
    'build',
    'connect:dist',
  ]);

  grunt.registerTask('default', [
    'serve'
  ]);

};