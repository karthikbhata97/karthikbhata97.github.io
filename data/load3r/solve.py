op = 'w2g1kS<c7me3keeuSMg1kSk%Se<=S3%/e/'
flags = '0100010011011101111111011010110101'

updated = ''
ans = ''

for c in op:
    updated += chr(ord(c)^5)


for a, f in zip(updated[::-1], flags):
    if f == '0':
        ans += chr(ord(a)<<1)
    else:
        ans += chr(ord(a)>>1)

print('inctf{%s}' % (ans,))