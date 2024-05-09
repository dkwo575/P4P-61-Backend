import axios from 'axios'

// Define the type for myAxios
const myAxios = axios.create({
    baseURL: 'http://localhost:5000',
    headers: {},
});

//请求拦截器
myAxios.interceptors.request.use(function(config){
    return config
},function (err){
    return Promise.reject(err)
})

//响应拦截器
myAxios.interceptors.request.use(function(response){
    return response
},function (err){
    return Promise.reject(err)
})

export default myAxios;
