var path = require('path');
var webpack = require('webpack');

var ExtractTextPlugin = require('extract-text-webpack-plugin');
var ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');
var CleanWebpackPlugin = require('clean-webpack-plugin');

var rootAssetPath = './app/assets';

config = {
    context: path.resolve(__dirname, './app/assets'),
    entry: {
        app_js: [
            'scripts/index'
        ],
        app_css: [
            'styles/main.scss'
        ]
    },
    output: {
        path: path.resolve(__dirname, './app/static/dist'),
        publicPath: 'http://localhost:2992/assets/',
        filename: '[name].[chunkhash].js',
        chunkFilename: '[id].[chunkhash].js'
    },
    resolve: {
        extensions: ['.js', '.css', '.scss'],
        modules: [
            path.resolve(__dirname, './app/assets/'),
            'node_modules'
        ],
    },
    module: {
        rules: [
            {
                test: /\.js$/i,
                use: [
                  'ng-annotate-loader',
                  'babel-loader'
                ],
                exclude: [/node_modules/],
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
                use: ['ngtemplate-loader?relativeTo=' + path.join(__dirname, rootAssetPath), 'raw-loader', 'html-minify-loader'],
                exclude: [/(node_modules)/]
            },
            {
                test: /\.woff2?$|\.ttf$|\.eot$|\.svg$/,
                use: ["file-loader"]
            },
            {
                test: /\.scss$/,
                use: ExtractTextPlugin.extract({
                  use: [
                    'css-loader', 'sass-loader'
                  ]
                })
            }
        ],
    },
    plugins: [
        new ExtractTextPlugin({
          filename:'[name].[chunkhash].css'
        }),
        new ManifestRevisionPlugin(path.join('app/static', 'manifest.json'), {
            rootAssetPath: rootAssetPath,
            ignorePaths: ['/styles', '/scripts']
        }),
    ]

};

if (process.env.NODE_ENV === 'production') {
    config.output.publicPath = '/static/dist/';
    config.plugins.push(new CleanWebpackPlugin(['app/static/dist/'], {
        verbose: true,
        dry: false
    }));
    config.plugins.push(new webpack.optimize.UglifyJsPlugin({
        compress: {
            warnings: false
        }
    }));
}


module.exports = config;
