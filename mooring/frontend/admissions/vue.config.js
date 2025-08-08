const { defineConfig } = require('@vue/cli-service');
const path = require('path');
const webpack = require('webpack');
// const MomentLocalesPlugin = require('moment-locales-webpack-plugin');
let port = process.env.PORT ? parseInt(process.env.PORT) : 8081;

module.exports = defineConfig({
    runtimeCompiler: true,
    outputDir: path.resolve(__dirname, '../../static/admissions_vue'),
    publicPath: '/static/admissions_vue/',
    filenameHashing: false,
    chainWebpack: (config) => {
        // config.resolve.alias.set("vue", "@vue/compat");
        // config.module
        //     .rule("vue")
        //     .use("vue-loader")
        //     .tap((options) => {
        //         return { ...options, compilerOptions: { compatConfig: { MODE: 2, }, }, };
        //     });
        config.resolve.alias.set('@vue-utils', path.resolve(__dirname, 'src/utils/vue'));
        config.resolve.alias.set('@common-utils', path.resolve(__dirname, 'src/components/common/'));
        config.resolve.alias.set('@static-root', path.resolve(__dirname, '../../../staticfiles/'));
    },
    configureWebpack: {
        entry: './src/main.js',
        devtool: 'source-map',
        resolve: {
            fallback: {
                buffer: require.resolve('buffer/'),
                stream: false,
                os: false
            },
        },
        plugins: [
            new webpack.ProvidePlugin({
                $: 'jquery',
                jQuery: 'jquery',
                moment: 'moment',
                swal: 'sweetalert2',
                _: 'lodash',
            }),
            // new MomentLocalesPlugin(),
            new webpack.ProvidePlugin({
                Buffer: ['buffer', 'Buffer'],
            }),
        ],
        devServer: {
            host: '0.0.0.0',
            allowedHosts: 'all',
            port: port,
            devMiddleware: {
                // Save file to disk so the Django server can serve them
                writeToDisk: true,
            },
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers':
                    'Origin, X-Requested-With, Content-Type, Accept',
            },
            client: {
                webSocketURL: 'ws://0.0.0.0:' + port + '/ws',
            },
            proxy: {
                '/api': {
                    target: 'http://127.0.0.1:9071',
                    changeOrigin: true,
                },
                '/admin': {
                    target: 'http://127.0.0.1:9071',
                    changeOrigin: true,
                }
            },
        },
        module: {
            rules: [
                /* config.module.rule('images') */
                {
                    test: /\.(png|jpe?g|gif|webp|avif)(\?.*)?$/,
                    type: 'asset/resource',
                    generator: {
                        filename: 'img/[name][ext]',
                    },
                },
                /* config.module.rule('fonts') */
                {
                    test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/i,
                    type: 'asset/resource',
                    generator: {
                        filename: 'fonts/[name][ext]',
                    },
                },
            ],
        },
        performance: {
            hints: false,
        },
    },
});