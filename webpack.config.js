var path = require('path');
var webpack = require('webpack');

var ExtractTextPlugin = require('extract-text-webpack-plugin');
var ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');

var rootAssetPath = './app/assets';

module.exports = {
    entry: {
        app_js: [
            rootAssetPath + '/scripts/index'
        ],
        app_css: [
            rootAssetPath + '/styles/main.scss'
        ]
    },
    output: {
        path: './app/static/dist',
        publicPath: 'http://localhost:2992/assets/',
        filename: '[name].[chunkhash].js',
        chunkFilename: '[id].[chunkhash].js'
    },
    resolve: {
        extensions: ['', '.js', '.css', '.scss'],
        modulesDirectories: [
            'node_modules'
        ],
        alias: {
            openlayers3: "openlayers/dist/ol.js",
        },
    },
    module: {
        loaders: [
            {
                test: /\.js$/i, loader: 'ng-annotate',
                exclude: /node_modules/
            },
            // {
            //     test: /\.(jpe?g|png|gif|svg([\?]?.*))$/i,
            //     loaders: [
            //         'file?context=' + rootAssetPath + '&name=[path][name].[hash].[ext]',
            //         'image?bypassOnDebug&optimizationLevel=7&interlaced=false'
            //     ]
            // },
            {
                test: /\.html$/,
                loaders: ['ngtemplate?relativeTo=' + path.join(__dirname, rootAssetPath), 'raw', 'html-minify'],
                exclude: /(node_modules)/
            },
            {
                test: /\.woff2?$|\.ttf$|\.eot$|\.svg$/,
                loader: "file"
            },
            {
                test: /\.scss$/,
                loader: ExtractTextPlugin.extract('style', 'css!sass')
            }
        ],
        noParse: [/dist\/ol.js/],
    },
    plugins: [
        new ExtractTextPlugin('[name].[chunkhash].css'),
        new ManifestRevisionPlugin(path.join('app/static', 'manifest.json'), {
            rootAssetPath: rootAssetPath,
            ignorePaths: ['/styles', '/scripts']
        }),
        new webpack.ProvidePlugin({
            ol: "openlayers3",
        })
    ]

};
