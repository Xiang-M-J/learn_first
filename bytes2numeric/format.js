function bytes2numeric(bytes, width, func) {
    const buffer = new ArrayBuffer(width)
    const ui8 = new Uint8Array(buffer)
    const numeric = new func(buffer)
    ui8.forEach(
        function (value, index, array) {
            array[index] = bytes[index]
        }
    )
    return numeric[0]
}
function bytes2bool(bytes) {
    const i32 = bytes2numeric(bytes, 4, Int32Array)
    return Boolean(i32)
}

function bytes2string(bytes, width) {
    const buffer = new ArrayBuffer(width)
    const ui8 = new Uint8Array(buffer)
    const decoder = new TextDecoder('utf-8')
    ui8.forEach(
        function (value, index, array) {
            array[index] = bytes[index]
        }
    )
    return decoder.decode(ui8)
}
