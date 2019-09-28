"""
IMPORTANT NOTE:
The running environment of this program is Python 3, instead of Python 2
Thanks.
"""

import re
import copy
import sys
class Vertex(object):
    def __init__(self, x, y):
        self.x_coordinate = float(x)
        self.y_coordinate = float(y)

    def __repr__(self):
        return '({0:.2f},{1:.2f})'.format(self.x_coordinate, self.y_coordinate)
    def __eq__(self, other):
        if self.x_coordinate==other.x_coordinate and self.y_coordinate==other.y_coordinate:
            return True
        return False
class Segment(object):
    def __init__(self, p1, p2):
        self.vertex_1 = p1
        self.vertex_2 = p2
    def __repr__(self):
        return '({0},{1})'.format(self.vertex_1,self.vertex_2)
    def __eq__(self, other):
        if self.vertex_1==other.vertex_1 and self.vertex_2==other.vertex_2:
            return True
        if self.vertex_1==other.vertex_2 and self.vertex_2==other.vertex_1:
            return True
        return False
class Street_segments(object):
    def __init__(self,name,segment):
        self.name=name
        self.segment=segment
        self.list = []
        self.list.append(self.segment)
    def __repr__(self):
        return '\"{0}\" {1}'.format(self.name,self.list)
    def add_a_segment(self, segment_2):
        self.list.append(segment_2)
    def delete_a_segment(self,segment):
        if segment in self.list:
            self.list.remove(segment)
        else:
            print("There is no such a segment in the street.")
    def length_of_segments(self):
        return len(self.list)

    def get_a_segment(self):
        #return the first segement and delete it
        if len(self.list)!=0:
            temp = self.list[0]
            self.list.remove(temp)
            return temp
        else:
            print("The street has no segment.")
    def output_first_segment(self):
        if len(self.list)!=0:
            return self.list[0]
    def output_ith_segment(self,i):
        return self.list[i]
class Street_vertices(object):
    def __init__(self,name,vertex):
        self.name=name
        self.vertex=vertex
        self.list=[]
        self.list.append(self.vertex)
    def __repr__(self):
        return '\"{0}\" {1}'.format(self.name,self.list)
    def add_a_vertex(self,vertex):
        self.list.append(vertex)
    def delete_a_vertex(self,vertex):
        if vertex in self.list:
            self.list.remove(vertex)
        else:
            print("There is no such a vertex in the street.")
    def get_a_vertex(self):
        if len(self.list)!=0:
            temp = self.list[0]
            self.list.remove(temp)
            return temp
        else:
            print("The street has no vertex.")
    def output_first_vertex(self):
        if len(self.list)!=0:
            return self.list[0]
    def length_of_vertices(self):
        return len(self.list)
class Street_vertices_set(object):
    def __init__(self,name,vertex):
        self.name=name
        self.vertex=vertex
        self.set=set()
        self.set.add(self.vertex)
    def __repr__(self):
        return '\"{0}\" {1}'.format(self.name,self.set)
    def add_a_vertex_set(self,vertex):
        self.set.add(vertex)
    def delete_a_vertex_set(self,vertex):
        if vertex in self.set:
            self.set.discard(vertex)
        else:
            print("There is no such a vertex in the street.")
    def length_of_vertices_set(self):
        return len(self.set)

streets_vertices_list=[]
streets_segments_list=[]

def input_parser():
    prompt="\nPlease input a command line:"
    prompt+="\nEnter 'q' to end the program.\n"
    i=""
    while i !='q':
        i = input(prompt)
        i = i.strip()
        a_command_re = re.compile("^a\s*\"(.*)\"\s*(\(.*\))$")
        c_command_re = re.compile("^c\s*\"(.*)\"\s*(\(.*\))$")
        r_command_re = re.compile("^r\s*\"(.*)\"$")
        g_command_re = re.compile("^g$")

        if a_command_re.match(i):
            add_a_street(i)
        elif c_command_re.match(i):
            change_a_street(i)
        elif r_command_re.match(i):
            remove_a_street(i)
        elif g_command_re.match(i):
            generate_a_street(find_all_intersections_1(streets_segments_list),find_all_intersections_2(streets_segments_list))
        elif i=='q':
            sys.exit(0)
        else:
            print("\nWrong input, input again!!")

def generate_a_street(streets_vertices_list_final, streets_segments_list_final_2):
    print("V = {")
    for i in streets_vertices_list_final:
        print("{0:.2f}_{1:.2f} : {2}".format(i.x_coordinate,i.y_coordinate,i))
        # print(f"{i.x_coordinate}_{i.y_coordinate} : {i}")
    print("}")

    print("E = {")
    for j in streets_segments_list_final_2:
        # print(f"<{j.vertex_1.x_coordinate}_{j.vertex_1.y_coordinate} , {j.vertex_2.x_coordinate}_{j.vertex_2.y_coordinate}>, ")
        print("<{0:.2f}_{1:.2f} , {2:.2f}_{3:.2f}>,".format(j.vertex_1.x_coordinate,j.vertex_1.y_coordinate,j.vertex_2.x_coordinate,j.vertex_2.y_coordinate))
    print("}")

def add_a_street_vertices(i):
    k=3
    while i[k] != '\"':
        k=k+1
    street_name=i[3:k]
    v=Vertex(1,1)
    sv=Street_vertices(street_name,v)
    sv.delete_a_vertex(v)
    # print(sv)
    while k<len(i):
        if i[k]=='(':
            # print(k)
            j=0
            while i[k+1]!=',':
                j=j+1
                k=k+1
            # print(i[k-j+1:k-j+j+1])
            vertex_x=float(i[k-j+1:k-j+j+1])

            m=0
            while  i[k]!=')':
                m=m+1
                k=k+1
            # print(i[k-m+2:k])
            vertex_y=float(i[k-m+2:k])
            # print(vertex_x)
            # vertex_y=int(i[k-1+3])
            sv.add_a_vertex(Vertex(vertex_x,vertex_y))
        k=k+1
    # print(sv)
    streets_vertices_list.append(sv)

def add_a_street_segments(i):
    streets_vertices_list_temp = []
    k = 3
    while i[k] != '\"':
        k = k + 1
    # type(k)
    street_name = i[3:k]
    v=Vertex(1,1)
    sv=Street_vertices(street_name,v)
    sv.delete_a_vertex(v)

    v1=Vertex(1,1)
    v2=Vertex(2,2)
    s=Segment(v1,v2)
    ss=Street_segments(street_name,s)
    # print(ss)
    ss.delete_a_segment(s)

    while k<len(i):
        if i[k]=='(':
            # print(k)
            j=0
            while i[k+1]!=',':
                j=j+1
                k=k+1
            # print(i[k-j+1:k-j+j+1])
            vertex_x=float(i[k-j+1:k-j+j+1])

            m=0
            while  i[k]!=')':
                m=m+1
                k=k+1
            # print(i[k-m+2:k])
            vertex_y=float(i[k-m+2:k])
            # print(vertex_x)
            # vertex_y=int(i[k-1+3])
            sv.add_a_vertex(Vertex(vertex_x,vertex_y))
        k=k+1
    streets_vertices_list_temp.append(sv)
    # print(streets_vertices_list_temp)
    for i in range(len(streets_vertices_list_temp)):
        sv= streets_vertices_list_temp[i]
        while len(sv.list)!=1:
            a=sv.output_first_vertex()
            sv.delete_a_vertex(a)
            # print(sv)
            b=sv.output_first_vertex()
            c=Segment(a,b)
            ss.add_a_segment(c)
    streets_segments_list.append(ss)
    # print(streets_segments_list)

def add_a_street(i):
    add_a_street_vertices(i)
    add_a_street_segments(i)
    # print(streets_vertices_list)
    # print(streets_segments_list)

def change_a_street(i):
    remove_a_street(i)
    add_a_street_vertices(i)
    add_a_street_segments(i)
    # print(streets_vertices_list)
    # print(streets_segments_list)
def remove_a_street(i):
    k=3
    while i[k] != '\"':
        k=k+1
    # type(k)
    street_name=i[3:k]
    # v=Vertex(1,1)
    # sv=Street_vertices(street_name,v)
    # sv.delete_a_vertex(v)
    # print (street_name)
    flag=0
    f=0
    for s in range(0,len(streets_vertices_list)):
        # print(s)
        # print(streets_vertices_list)
        if  flag==0 and streets_vertices_list[s].name==street_name:
            streets_vertices_list.remove(streets_vertices_list[s])
            flag=1
    for t in range(0,len(streets_segments_list)):
        if f==0 and streets_segments_list[t].name==street_name:
            streets_segments_list.remove(streets_segments_list[t])
            f=1
    # print(streets_vertices_list)
    # print(streets_segments_list)
    # find_all_intersections(streets_segments_list)

def get_intersection(segment_1,segment_2):
    x1 = segment_1.vertex_1.x_coordinate
    y1 = segment_1.vertex_1.y_coordinate
    x2 = segment_1.vertex_2.x_coordinate
    y2 = segment_1.vertex_2.y_coordinate
    x3 = segment_2.vertex_1.x_coordinate
    y3 = segment_2.vertex_1.y_coordinate
    x4 = segment_2.vertex_2.x_coordinate
    y4 = segment_2.vertex_2.y_coordinate
    try:
        p1= ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        q1 = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
                (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    except ZeroDivisionError:
        return None
    # else:
        # print(p1)
        # print(q1)
    if max(min(x1,x2),min(x3,x4))<=p1<=min(max(x1,x2),max(x3,x4)) and max(min(y1,y2),min(y3,y4))<=q1<=min(max(y1,y2),max(y3,y4)):
        return Vertex(p1,q1)

def find_all_intersections_1(streets_segments_list):
    intersections_list=[]
    streets_vertices_list_final = []
    streets_segments_list_final_2 = []
    streets_segments_list_final = []
    streets_segments_list_temp=copy.deepcopy(streets_segments_list)
    # print(streets_segments_list)
    # print(len(streets_segments_list))
    streets_segments_length=len(streets_segments_list)
    for i in range(0,streets_segments_length):
        # print(streets_segments_list[i].length_of_segments())
        for j in range(0,streets_segments_list[i].length_of_segments()):
            first_segment = streets_segments_list_temp[i].get_a_segment()
            # print(first_segment)
            # streets_segments_list[i].delete_a_segment(first_segment)
            for m in range(i+1,streets_segments_length):
                for k in range(0,streets_segments_list[m].length_of_segments()):
                    second_segment = streets_segments_list_temp[m].output_ith_segment(k)
                    # print(first_segment)
                    # print(second_segment)
                    # print("____")
                    intersection = get_intersection(first_segment, second_segment)
                    # print(type(intersection))
                    if intersection is not None:
                        # print(intersection)
                        # print(f"----------------{intersections_list}")
                        if intersection not in intersections_list:
                            intersections_list.append(intersection)
                        if intersection not in streets_vertices_list_final:
                            streets_vertices_list_final.append(intersection)
                        if first_segment.vertex_1 not in streets_vertices_list_final:
                            streets_vertices_list_final.append((first_segment.vertex_1))
                        if first_segment.vertex_2 not in streets_vertices_list_final:
                            streets_vertices_list_final.append((first_segment.vertex_2))
                        if second_segment.vertex_1 not in streets_vertices_list_final:
                            streets_vertices_list_final.append((second_segment.vertex_1))
                        if second_segment.vertex_2 not in streets_vertices_list_final:
                            streets_vertices_list_final.append((second_segment.vertex_2))

                        if Segment(intersection, first_segment.vertex_1) not in streets_segments_list_final:
                            streets_segments_list_final.append(Segment(intersection, first_segment.vertex_1))
                        if Segment(intersection, first_segment.vertex_2) not in streets_segments_list_final:
                            streets_segments_list_final.append(Segment(intersection, first_segment.vertex_2))
                        if Segment(intersection, second_segment.vertex_1) not in streets_segments_list_final:
                            streets_segments_list_final.append(Segment(intersection, second_segment.vertex_1))
                        if Segment(intersection, second_segment.vertex_2) not in streets_segments_list_final:
                            streets_segments_list_final.append(Segment(intersection, second_segment.vertex_2))
    # print(intersections_list)
    # print(streets_vertices_list_final)
    # print(streets_segments_list_final)
    streets_segments_list_final_final=intersection_in_final_segment(intersections_list,streets_segments_list_final)
    temp_list=delete_duplicate(streets_segments_list_final_final)
    for a in temp_list:
        streets_segments_list_final_2.append(a)
    return streets_vertices_list_final

def find_all_intersections_2(streets_segments_list):
    intersections_list=[]
    streets_vertices_list_final = []
    streets_segments_list_final_2 = []
    streets_segments_list_final = []

    streets_segments_list_temp=copy.deepcopy(streets_segments_list)
    # print(streets_segments_list)
    # print(len(streets_segments_list))
    streets_segments_length=len(streets_segments_list)
    for i in range(0,streets_segments_length):
        # print(streets_segments_list[i].length_of_segments())
        for j in range(0,streets_segments_list[i].length_of_segments()):
            first_segment = streets_segments_list_temp[i].get_a_segment()
            # print(first_segment)
            # streets_segments_list[i].delete_a_segment(first_segment)
            for m in range(i+1,streets_segments_length):
                for k in range(0,streets_segments_list[m].length_of_segments()):
                    second_segment = streets_segments_list_temp[m].output_ith_segment(k)
                    # print(first_segment)
                    # print(second_segment)
                    # print("____")
                    intersection = get_intersection(first_segment, second_segment)
                    # print(type(intersection))
                    if intersection is not None:
                        # print(intersection)
                        if intersection not in intersections_list:
                            intersections_list.append(intersection)
                        if intersection not in streets_vertices_list_final:
                            streets_vertices_list_final.append(intersection)
                        if first_segment.vertex_1 not in streets_vertices_list_final:
                            streets_vertices_list_final.append((first_segment.vertex_1))
                        if first_segment.vertex_2 not in streets_vertices_list_final:
                            streets_vertices_list_final.append((first_segment.vertex_2))
                        if second_segment.vertex_1 not in streets_vertices_list_final:
                            streets_vertices_list_final.append((second_segment.vertex_1))
                        if second_segment.vertex_2 not in streets_vertices_list_final:
                            streets_vertices_list_final.append((second_segment.vertex_2))

                        if Segment(intersection, first_segment.vertex_1) not in streets_segments_list_final:
                            streets_segments_list_final.append(Segment(intersection, first_segment.vertex_1))
                        if Segment(intersection, first_segment.vertex_2) not in streets_segments_list_final:
                            streets_segments_list_final.append(Segment(intersection, first_segment.vertex_2))
                        if Segment(intersection, second_segment.vertex_1) not in streets_segments_list_final:
                            streets_segments_list_final.append(Segment(intersection, second_segment.vertex_1))
                        if Segment(intersection, second_segment.vertex_2) not in streets_segments_list_final:
                            streets_segments_list_final.append(Segment(intersection, second_segment.vertex_2))
    # print(intersections_list)
    # print(streets_vertices_list_final)
    # print(streets_segments_list_final)
    streets_segments_list_final_final=intersection_in_final_segment(intersections_list,streets_segments_list_final)
    temp_list=delete_duplicate(streets_segments_list_final_final)
    for a in temp_list:
        streets_segments_list_final_2.append(a)
    return streets_segments_list_final_2

def delete_duplicate(list_of_street_segments):
    l=[]
    for i in list_of_street_segments:
        if i not in l:
            l.append(i)
    return l

def intersection_in_final_segment(intersections_list, streets_segments_list_final):
    streets_segments_list_final_temp=copy.deepcopy(streets_segments_list_final)
    for i in intersections_list:
        for j in streets_segments_list_final_temp:
            if intersecion_in_line(i,j):
                streets_segments_list_final_temp.remove(j)
                streets_segments_list_final_temp.append(Segment(i,j.vertex_1))
                streets_segments_list_final_temp.append(Segment(i,j.vertex_2))
    return streets_segments_list_final_temp

def intersecion_in_line(intersection,line):
    # if (intersection.y_coordinate-line.vertex_2.y_coordinate)/(line.vertex_1.y_coordinate-line.vertex_2.y_coordinate)==(intersection.x_coordinate-line.vertex_2.x_coordinate)/(line.verter_1.x_coordinate-line.verterx_2.x_coordinate) and min(line.verter_1.x_coordinate,line.verterx_2.x_coordinate)<intersection.x_coordinate<max(line.verter_1.x_coordinate,line.verterx_2.x_coordinate):
    try: (intersection.y_coordinate - line.vertex_2.y_coordinate) / (
            line.vertex_1.y_coordinate - line.vertex_2.y_coordinate) == (
            intersection.x_coordinate - line.vertex_2.x_coordinate) / (
            line.vertex_1.x_coordinate - line.vertex_2.x_coordinate) and min(line.vertex_1.x_coordinate,
                                                                              line.vertex_2.x_coordinate) < intersection.x_coordinate < max(
        line.vertex_1.x_coordinate, line.vertex_2.x_coordinate)
    except ZeroDivisionError:
        # if (line.vertex_1.x_coordinate==line.vertex_2.x_coordinate and line.vertex_2.x_coordinate==intersection.x_coordinate) and min(line.vertex_1.y_coordinate,line.vertex_2.y_coordinate)<intersection.y_coordinate<max(line.vertex_1.y_coordinate,line.vertex_2.y_coordinate):
        if(
                    line.vertex_1.x_coordinate == line.vertex_2.x_coordinate and line.vertex_2.x_coordinate == intersection.x_coordinate) and min(
            line.vertex_1.y_coordinate, line.vertex_2.y_coordinate) < intersection.y_coordinate < max(
            line.vertex_1.y_coordinate, line.vertex_2.y_coordinate):
            return True
        if (line.vertex_1.y_coordinate==line.vertex_2.y_coordinate and line.vertex_2.y_coordinate==intersection.y_coordinate) and min(line.vertex_1.x_coordinate,line.vertex_2.x_coordinate)<intersection.x_coordinate<max(line.vertex_1.x_coordinate,line.vertex_2.x_coordinate):
            return True
        return False
    else:
        if (intersection.y_coordinate - line.vertex_2.y_coordinate) / (
                line.vertex_1.y_coordinate - line.vertex_2.y_coordinate) == (
                intersection.x_coordinate - line.vertex_2.x_coordinate) / (
                line.vertex_1.x_coordinate - line.vertex_2.x_coordinate) and min(line.vertex_1.x_coordinate,
                                                                                  line.vertex_2.x_coordinate) < intersection.x_coordinate < max(
            line.vertex_1.x_coordinate, line.vertex_2.x_coordinate):
            return True
        else:
            return False

def remove_duplicates_intersection(vertices_list):
    final_list=[]
    for i in vertices_list:
        # print(i)
        for j in range(0,len(final_list)):
            if i !=final_list[j]:
                final_list.append(i)
                print(final_list)
    return final_list

def main():
    input_parser()
    # l=copy.deepcopy(streets_segments_list)
    # print(streets_vertices_list_final)
    # print(streets_segments_list_final_2)
    # print(l)

    # generate_final_edges(a)

if __name__ == '__main__':
    main()


"""
input example:
a "Weber Street" (2,-1) (2, 2) (5, 5) (5,6)(3,8)
a "King Street S" (4,2) (4,8) 
a "Davenport Road" (1,4) (5,8)
c "Weber Street" (2,1) (2,2)
r "King Street S"

c "Weber Street" (2,-1) (2, 2) (5, 5) (5,6)(3,8)

a "Weber Street" (2,1) (2,2)

a "a" (3,8) (3,0)
a "b" (0,2) (4,2)
a "c" (1,4) (5,4)
a "d" (1,8) (5,8)
a "e" (0,0) (3,8)



"""


