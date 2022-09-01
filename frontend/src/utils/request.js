import axios from 'axios'
import { Message } from 'element-ui'

// create an axios instance
const service = axios.create({
  // baseURL: 'http://0.0.0.0:/9050',
  // baseURL: 'http://101.6.69.215:9050/', 
  baseURL: 'http://47.100.99.53:9050/', 
  // baseURL: 'http://101.6.69.238:5000/', // url = base url + request url
  // baseURL: 'http://101.6.68.147:5000/', // url = base url + request url
  // baseURL: 'http://127.0.0.1:5000/', // url = base url + request url
  // baseURL: 'http://localhost:5000/', // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 5000 // request timeout
})

// request interceptor
service.interceptors.request.use(
  config => {
    // do something before request is sent
    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
  */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  response => {
    const res = response.data
    return res
  },
  error => {
    console.log(error) // for debug
    Message({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
