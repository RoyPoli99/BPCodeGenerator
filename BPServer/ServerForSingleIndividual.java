import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import org.json.JSONObject;

import java.io.*;
import java.net.InetSocketAddress;

public class ServerForSingleIndividual implements HttpHandler {

    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);
        server.createContext("/TicTacToe", new ServerForSingleIndividual());
        server.setExecutor(GA_Solver.executorService); // creates a default executor
        server.start();
    }

    @Override
    public void handle(HttpExchange httpExchange) throws IOException {
        InputStream res = httpExchange.getRequestBody();
        BufferedReader in = new BufferedReader(
                new InputStreamReader(res));
        String inputLine;
        StringBuffer content = new StringBuffer();
        while ((inputLine = in.readLine()) != null) {
            content.append(inputLine);
        }
        in.close();
        JSONObject obj = new JSONObject(content.toString());
        String[] currentSolution = new String[10];
        for(int i = 0; i < 10; i++){
            currentSolution[i] = obj.getString("t" + i);
        }
        int randomPlayer = obj.getInt("rand");
        boolean playAgainstRandomPlayer = randomPlayer == 1;

        GPSimulator simulator = new GPSimulator(currentSolution, GA_Solver.executorService, playAgainstRandomPlayer);

        String response = "" + simulator.getFitness();
        System.out.println(response);

        httpExchange.sendResponseHeaders(200, response.length());
        OutputStream os = httpExchange.getResponseBody();
        os.write(response.getBytes());
        os.close();
    }

}
