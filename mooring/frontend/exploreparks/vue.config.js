const { defineConfig } = require('@vue/cli-service');
const path = require('path');
const webpack = require('webpack');

// Define the port for the development server, using an environment variable if available.
let port = process.env.PORT ? parseInt(process.env.PORT) : 8083;

module.exports = defineConfig({
    runtimeCompiler: true,

    // Specify the output directory for the production build.
    // This is configured to point to a Django static files directory.
    outputDir: path.resolve(__dirname, '../../static/exploreparks'),

    // Set the public path for deployed assets.
    // This should match Django's STATIC_URL configuration for this app.
    publicPath: '/static/exploreparks/',

    // Disable filename hashing to produce predictable file names (e.g., app.js).
    filenameHashing: false,

    // Use chainWebpack for fine-grained control over the internal Webpack configuration.
    chainWebpack: (config) => {
        // config.resolve.alias.set("vue", "@vue/compat");
        // config.module
        //     .rule("vue")
        //     .use("vue-loader")
        //     .tap((options) => {
        //         return { ...options, compilerOptions: { compatConfig: { MODE: 2, }, }, };
        //     });
        // Set up path aliases for cleaner and easier imports.
        config.resolve.alias.set('@vue-utils', path.resolve(__dirname, 'src/utils/vue'));
        config.resolve.alias.set('@common-utils', path.resolve(__dirname, 'src/components/common/'));
        config.resolve.alias.set('@static-root', path.resolve(__dirname, '../../../staticfiles/'));
    },

    // Directly modify or extend the Webpack configuration.
    configureWebpack: {
        // Define the entry point of the application.
        entry: './src/main.js',

        // Generate source maps for easier debugging in development.
        devtool: 'source-map',

        // Provide fallbacks (polyfills) for Node.js core modules to ensure browser compatibility.
        resolve: {
            fallback: {
                buffer: require.resolve('buffer/'),
                stream: false,
                os: false
            },
        },

        // Configure Webpack plugins.
        plugins: [
            // This plugin makes jQuery available to all modules without needing to import it everywhere.
            new webpack.ProvidePlugin({
                $: 'jquery',
                jQuery: 'jquery',
                moment: 'moment',
                swal: 'sweetalert2',
                _: 'lodash',
            }),
            // Provides the Buffer class as a polyfill. 
            new webpack.ProvidePlugin({
                Buffer: ['buffer', 'Buffer'],
            }),
        ],

        // Configure the development server.
        devServer: {
            host: '0.0.0.0', // Allow access from the network.
            allowedHosts: 'all', // Allow all hosts to connect
            port: port,
            devMiddleware: {
                // Write bundled files to disk, useful for Django to serve them during development.
                writeToDisk: true,
            },
            // Set custom headers, e.g., for CORS (Cross-Origin Resource Sharing).
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers':
                    'Origin, X-Requested-With, Content-Type, Accept',
            },
            // Configure the WebSocket URL for Hot Module Replacement (HMR).
            client: {
                webSocketURL: 'ws://0.0.0.0:' + port + '/ws',
            },
            // Proxy API requests to the backend server to avoid CORS issues during development.
            proxy: {
                '/api': {
                    target: 'http://127.0.0.1:9071',
                    changeOrigin: true,
                },
                '/admin': {
                    target: 'http://127.0.0.1:9071',
                    changeOrigin: true,
                }
            }
        },

        // Define rules for how different types of modules (files) are treated.
        module: {
            rules: [
                // Rule for handling image files.
                {
                    test: /\.(png|jpe?g|gif|webp|avif)(\?.*)?$/,
                    type: 'asset/resource',
                    generator: {
                        // Output images to the 'img/' subfolder with their original names.
                        filename: 'img/[name][ext]',
                    },
                },
                // Rule for handling font files.
                {
                    test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/i,
                    type: 'asset/resource',
                    generator: {
                        // Output fonts to the 'fonts/' subfolder with their original names.
                        filename: 'fonts/[name][ext]',
                    },
                },
            ],
        },

        // Disable performance hints to prevent warnings about asset sizes.
        performance: {
            hints: false,
        },
    },
});