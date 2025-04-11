// FV = P [ (1+i)^n-1 ] * (1+i)/i
// i = r/100
// 2000 * [(1+0.01) ^24 - 1] * (1+0.01)/0.01

var amt = 2000                  // p
var months = 24                    // n
var rate =  parseFloat(12/100/12)  // i
console.log("rate",rate);

// var math = Math.pow((1 + rate), (months- 1))
// var In = parseFloat(1+ rate)/rate
// var Intrest = Amount * math * In
// var Total = Intrest + Amount

total = amt * [ (1+rate) ** months-1 ] * (1+rate)/rate

console.log("return",total)
