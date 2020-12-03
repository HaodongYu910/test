<el-dialog title="匿名化文件夹" :visible.sync="addFormVisible" :close-on-click-modal="false"
                       style="width: 75%; left: 12.5%">
                <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
                    <el-form :inline="true" :model="filters" @submit.native.prevent>
                        <el-row>


                            <el-col :span="5">
                                <el-form-item label="发送服务器" prop="sendserver">
                                    <el-select v-model="addForm.sendserver" placeholder="请选择"
                                               @click.native="gethost()">
                                        <el-option
                                                v-for="(item,index) in tags"
                                                :key="item.host"
                                                :label="item.name"
                                                :value="item.host"
                                        />
                                    </el-select>
                                </el-form-item>
                            </el-col>
                            <el-col :span="3">
                                <el-form-item label="端口号" prop="port">
                                    <el-input id="port" v-model="addForm.port" placeholder=""/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="6">
                                <el-form-item label="数据类型" prop="senddata">
                                    <el-select v-model="addForm.senddata" multiple placeholder="请选择"
                                               @click.native="getBase()">
                                        <el-option
                                                v-for="(item,index) in tags"
                                                :key="item.remarks"
                                                :label="item.remarks"
                                                :value="item.remarks"
                                        />
                                    </el-select>
                                </el-form-item>
                            </el-col>
                            <el-col :span="4">
                                <el-form-item label="匿名名称" prop="keyword">
                                    <el-input id="keyword" v-model="addForm.keyword" placeholder="数据名称"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="3">
                                <el-form-item label="持续时间" prop="loop_time">
                                    <el-input id="loop_time" v-model="addForm.loop_time" placeholder="小时"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="3">
                                <el-form-item label="发送数量" prop="count">
                                    <el-input id="sendcount" v-model="addForm.sendcount" placeholder="共/个"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="4">
                                <el-form-item label="延时时间" prop="sleeptime">
                                    <el-input id="sleeptime" v-model="addForm.sleeptime" placeholder="秒"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="4">
                                <el-form-item label="延时数量" prop="sleepcount">
                                    <el-input id="sleepcount" v-model="addForm.sleepcount" placeholder="张"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="3">
                                <el-form-item label="series" prop="series">
                                    <el-switch v-model="addForm.series" active-color="#13ce66"
                                               inactive-color="#ff4949"></el-switch>
                                </el-form-item>
                            </el-col>
                            <el-col :span="6">
                                <el-form-item label="" prop="dds">
                                    <el-input id="dds" v-model="addForm.dds" placeholder="DDS服务"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="4">
                                <el-form-item label="" prop="save">
                                    <el-button type="primary" @click="addSubmit('form')">保存</el-button>
                                </el-form-item>
                            </el-col>
                        </el-row>
                    </el-form>
                </el-form>
            </el-dialog>


<el-dialog title="匿名化文件夹" :visible.sync="addFormVisible" :close-on-click-modal="false"
                       style="width: 75%; left: 12.5%">
                <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
                    <el-form :inline="true" :model="filters" @submit.native.prevent>
                        <el-row>
                            <el-col :span="4">
                                <el-form-item label="匿名名称" prop="keyword">
                                    <el-input id="keyword" v-model="addForm.keyword" placeholder="数据名称"/>
                                </el-form-item>
                            </el-col>

                            <el-col :span="4">
                                <el-form-item label="需要被匿名文件路径" prop="keyword">
                                    <el-input id="keyword" v-model="addForm.keyword" placeholder="数据名称"/>
                                </el-form-item>
                            </el-col>

</el-row>
                    </el-form>
                </el-form>
            </el-dialog>