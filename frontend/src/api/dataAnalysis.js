import request from '@/utils/request.js'

export function getTextAnalysis(data) {
  return request({
    url: '/api/v1/getTextAnalysis',
    method: 'post',
    data
  })
}

export function getDailyInfo(data) {
  return request({
    url: '/api/v1/getDailyInfo1',
    method: 'post',
    data
  })
}

export function getAnalysisInfo(data) {
  return request({
    url: '/api/v1/getAnalysisInfo1',
    method: 'post',
    data
  })
}

export function getAnalysisDetail(data) {
  return request({
    url: '/api/v1/getAnalysisDetail1',
    method: 'post',
    data
  })
}

export function getSentimentAnalysis(data) {
  return request({
    url: '/api/v1/getSentimentAnalysis',
    method: 'post',
    data
  })
}

export function getTriplets(data) {
  return request({
    url: '/api/v1/getTriplets',
    method: 'post',
    data
  })
}
