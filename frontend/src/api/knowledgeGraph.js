import request from '@/utils/request.js'

export function getProductGraph(data) {
  return request({
    url: '/api/v1/getProductGraph',
    method: 'post',
    data
  })
}
