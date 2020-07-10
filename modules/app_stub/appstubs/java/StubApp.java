import java.util.concurrent.TimeUnit ;
// import com.newrelic.api.agent.Trace;


public class StubApp {
    // @Trace(dispatcher=true)
    public static void main(String[] args)  throws InterruptedException {
        TimeUnit.SECONDS.sleep(5);
    }

}