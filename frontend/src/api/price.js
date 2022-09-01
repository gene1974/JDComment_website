import request from '@/utils/request.js'

export function fetchBoxInfo() {
  return request({
    url: '/api/v1/boxInfo',
    method: 'get',
  })
}

export function fetchPigPriceDiffArea() {
  return request({
    url: '/api/v1/pigPriceDiffArea',
    method: 'get',
  })
}

export function fetchPigPrice() {
  return request({
    url: '/api/v1/pigPrice',
    method: 'get',
  })
}

export function fetchPorkPricePerDay() {
  return request({
    url: '/api/v1/porkPricePerDay',
    method: 'get',
  })
}

export function fetchPorkPricePerWeek() {
  return request({
    url: '/api/v1/porkPricePerWeek',
    method: 'get',
  })
}

export function fetchPorkPricePerMonth() {
  return request({
    url: '/api/v1/porkPricePerMonth',
    method: 'get',
  })
}

export function fetchPorkPricePer5Days(timeSpan) {
  return request({
    url: '/api/v1/porkPricePer5Days',
    method: 'get',
    params: { timeSpan }, 
  })
}

