import request from '@/utils/request.js'

export function fetchNextText(data) {
  return request({
    url: '/api/v1/getNextText',
    method: 'post',
    data
  })
}

export function fetchHistory() {
  return request({
    url: '/api/v1/getOneHistory',
    method: 'get',
  })
}

export function fetchPageHistory(data) {
  return request({
    url: '/api/v1/getPageHistory',
    method: 'post',
    data
  })
}

export function fetchPageHistoryFiltered(data) {
  return request({
    url: '/api/v1/getPageHistoryFiltered',
    method: 'post',
    data
  })
}

export function fetchHistoryInfo(data) {
  return request({
    url: '/api/v1/getHistoryInfo',
    method: 'post',
    data
  })
}

export function postEvent(data) {
  return request({
    url: '/api/v1/postEvent',
    method: 'post',
    data
  })
}

export function fetchEventLabeledCount(data) {
  return request({
    url: '/api/v1/annotationRecord',
    method: 'post',
    data
  })
}
