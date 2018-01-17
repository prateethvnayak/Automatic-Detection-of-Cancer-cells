import tensorflow as tf, sys
import list_files as lf

def predict(crop_path):
    crop_dir = crop_path # send the image path to this ( the cropped single cell)
    crop_list = lf.img_list(crop_dir)

    label_lines = [line.rstrip() for line in tf.gfile.GFile("ROOT DIRECTORY NAME/abnormal_normal.txt")]  # enter the path to .txt label file

    with tf.gfile.FastGFile("ROOT DIRECTORY NAME/50000itr/retrained_graph.pb", 'rb') as f:  # enter the .pb model path
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name="")

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        n = []
        s = []
        for i in range(0, crop_list.__len__()):
            path = crop_dir + "/" + crop_list[i]
            img_data = tf.gfile.FastGFile(path, 'rb').read()
            predictions = sess.run(softmax_tensor, {"DecodeJpeg/contents:0": img_data})
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            print "For image ", i+1

            for node_id in top_k:
                human_string = label_lines[node_id]
                score = predictions[0][node_id]
                if score > 0.50:
                    print ("%s (score = %0.5f)" % (human_string, score))
                    if human_string == label_lines[0]:
                        n.append(1)
                    elif human_string == label_lines[1]:
                        n.append(0)
                    s.append(score)
    return n, s

		
