const config = require('./src/config');
     
config.runServer(

    process.argv[2],   // host
    parseInt(process.argv[3])          // port

)