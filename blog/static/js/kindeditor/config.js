//config.js
KindEditor.ready(function(K) {
    K.create('#id_body',{
        // 指定大小
        width:'680px',
        height:'300px',
        uploadJson: '/admin/upload/kindeditor',
    });
});