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
      app: require('./bower.json').appPath || './',
      dist: 'dist'
    },
		handlebars: {
		  compile: {
		    options: {
		      namespace: "JST",
		      amd: true,
					processName: function (filePath) {
						var file = filePath.replace('scripts/templates/','');
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
		      "scripts/JST.js": ["scripts/templates/**/*.handlebars"]
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
    }
  });

  // By default, lint and run all tests.
  grunt.registerTask('dev', [
    // 'compass',
    // 'concurrent:dev'
  ]);

  grunt.registerTask('serve', [
    // 'compass',
    // 'handlebars',
    // 'uglify',
    'connect:livereload'
  ]);

  // Setting up dummy task for grunt to build the dist folder
  grunt.registerTask('build', [
    // 'clean:dist',
    // 'concurrent:dist',
    // 'concat',
    // 'cssc:build',
    // 'cssmin:build',
    // 'handlebars',
    // 'uglify',
    // // 'imagemin:build',
    // 'copy:dist'
  ]);

  grunt.registerTask('default', [
    // 'newer:jshint',
    // 'test',
    // 'build'
  ]);

};