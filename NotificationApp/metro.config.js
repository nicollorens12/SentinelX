const {getDefaultConfig} = require('metro-config');

module.exports = {
    server: {
      usePolling: true, // Esto activa el polling en lugar de watch
    },
  };
  
